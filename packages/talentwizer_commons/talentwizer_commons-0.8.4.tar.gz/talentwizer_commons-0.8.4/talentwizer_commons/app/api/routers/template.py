from fastapi import APIRouter, HTTPException, Body, Path
from pydantic import BaseModel, Field, model_validator  # Change validator to model_validator
from typing import List, Optional
from bson import ObjectId
from talentwizer_commons.utils.db import mongo_database
from talentwizer_commons.utils.email import (
    schedule_email, 
    populate_template_v2, 
    populate_template_v1,
    send_email_from_user_email,
    EmailPayload
)
from talentwizer_commons.utils.celery_init import get_test_delay  # Add this import
import os
from datetime import datetime, timedelta
import pytz
import logging
import traceback

# Configure logging
logger = logging.getLogger("talentwizer_commons.app.api")

template_router = t = APIRouter()

# MongoDB Setup - use existing mongo_database instead of motor
template_collection = mongo_database["templates"]
variable_collection = mongo_database["variables"]
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

# Helper function to convert MongoDB ObjectId to string
def to_dict(document):
    """Convert MongoDB document to a dictionary with stringified `_id`."""
    document["_id"] = str(document["_id"])
    return document

# Pydantic Models
class SequenceStep(BaseModel):
    sendingTime: str = Field(..., title="Sending Time")
    sender: str = Field(..., title="Sender")
    subject: str = Field(..., title="Subject")
    content: str = Field(..., title="Content")
    variables: List[str] = Field(..., title="Variables")
    aiCommands: List[str] = Field(..., title="AI Smart Commands")
    unsubscribe: bool = Field(..., title="Unsubscribe")
    emailSignature: str = Field(..., title="Email Signature")
    days: Optional[int] = None  # Make these optional
    time: Optional[str] = None
    timezone: Optional[str] = None
    dayType: Optional[str] = None
    is_initial: bool = False  # Whether this is first email in thread
    thread_id: Optional[str] = None  # For tracking email thread

    @model_validator(mode='before')
    def validate_time_fields(cls, values):
        """Validate time-related fields based on sendingTime value."""
        if values.get('sendingTime') == 'immediate':
            values['days'] = None
            values['time'] = None
            values['timezone'] = None
            values['dayType'] = None
        return values

class Template(BaseModel):
    id: str = Field(None, alias="_id")  # Use alias to map `_id` field from MongoDB
    name: str = Field(..., title="Template Name", max_length=100)
    steps: List[SequenceStep] = Field(..., title="Sequence Steps")

    class Config:
        populate_by_name = True

class TemplateUpdate(BaseModel):
    name: str | None = Field(None, title="Template Name", max_length=100)
    steps: List[SequenceStep] | None = Field(None, title="Sequence Steps")

class Variable(BaseModel):
    _id: str
    name: str = Field(..., title="Variable Name", max_length=100)

class EmailScheduleRequest(BaseModel):
    profile_ids: List[str]
    template_id: str
    job_title: str
    tokenData: dict  # Add token data field

class EmailSequence(BaseModel):
    profile_id: str
    template_id: str
    public_identifier: str
    sequence_steps: List[dict]
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EmailSequenceAudit(BaseModel):
    sequence_id: str
    step_index: int
    template_id: str
    profile_id: str
    public_identifier: str
    email_payload: dict
    scheduled_time: datetime
    status: str  # SCHEDULED, SENT, FAILED
    sent_time: Optional[datetime] = None  # Make it optional with None as default
    error_message: Optional[str] = None   # Make it optional with None as default
    created_at: datetime = Field(default_factory=datetime.utcnow)
    token_data: Optional[dict] = None  # Add this field to allow token data
    thread_id: Optional[str] = None
    is_initial: bool = False
    replied: bool = False
    unsubscribed: bool = False

    class Config:
        validate_assignment = True
        extra = 'forbid'

@t.get("/variables", response_model=List[Variable], summary="Fetch all predefined variables")
async def get_variables():
    variables = list(variable_collection.find())
    return [to_dict(variable) for variable in variables]

@t.post("/variables/", response_model=Variable, summary="Create a new predefined variable")
async def create_variable(variable: Variable):
    variable_dict = variable.dict()
    result = variable_collection.insert_one(variable_dict)
    if result.inserted_id:
        return to_dict({**variable_dict, "_id": result.inserted_id})
    raise HTTPException(status_code=500, detail="Failed to create variable")

@t.get("/sending-time-options", summary="Fetch sending time options")
async def get_sending_time_options():
    options = [
        {"label": "Immediate", "value": "immediate"},
        {"label": "Next Business Day", "value": "next_business_day"},
        {"label": "After", "value": "after"}
    ]
    return options

# Routes
@t.get("/", response_model=List[Template], summary="Fetch all templates")
async def get_templates():
    templates = list(template_collection.find())
    # Convert ObjectId to string for JSON serialization
    for template in templates:
        if "_id" in template:
            template["_id"] = str(template["_id"])
    return templates

@t.get("/{id}", response_model=Template, summary="Fetch a template by ID")
async def get_template_by_id(
    id: str = Path(..., title="Template ID", description="ID of the template to fetch")
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    template = template_collection.find_one({"_id": ObjectId(id)})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return to_dict(template)

@t.post("/", response_model=Template, summary="Create a new template")
async def create_template(template: Template):
    template_dict = template.dict(exclude={"_id"})  # Exclude _id on create
    result = template_collection.insert_one(template_dict)
    if result.inserted_id:
        return to_dict({**template_dict, "_id": result.inserted_id})
    raise HTTPException(status_code=500, detail="Failed to create template")

@t.put("/{id}", response_model=Template, summary="Edit an existing template")
async def edit_template(
    id: str = Path(..., title="Template ID", description="ID of the template to edit"),
    update_data: TemplateUpdate = Body(...)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    update_data_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_data_dict:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    result = template_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data_dict},
        return_document=True
    )
    if result:
        return to_dict(result)
    raise HTTPException(status_code=404, detail="Template not found")

@t.delete("/{id}", summary="Delete a template")
async def delete_template(
    id: str = Path(..., title="Template ID", description="ID of the template to delete")
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    result = template_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Template deleted successfully"}
    raise HTTPException(status_code=404, detail="Template not found")

def calculate_next_business_day(date: datetime) -> datetime:
    """Calculate the next business day from a given date."""
    next_day = date + timedelta(days=1)
    while next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        next_day += timedelta(days=1)
    
    # Set time to beginning of business day (e.g., 9:00 AM)
    next_day = next_day.replace(hour=9, minute=0, second=0, microsecond=0)
    return next_day

# async def process_sequence_for_person(person: dict, template: dict, step: dict, job_title: str,  client_info: Optional[dict] = None) -> dict:
#     """Process a template sequence step for a person."""
#     logger.info(f"Processing template for {person.get('public_identifier')}")
#     try:
#         # Get primary email
#         email = person.get("email", [])
#         if isinstance(email, list):
#             email = email[0] if email else None
        
#         if not email:
#             return {
#                 "status": "error",
#                 "message": f"No email found for profile {person['public_identifier']}"
#             }

#         # Replace variables in template content using the provided job_title
#         email_content = await populate_template_v2(step["content"], person, job_title, client_info)
#         subject = await populate_template_v2(step["subject"], person, job_title, client_info)
        
#         email_payload = {
#             "to_email": [email],
#             "subject": subject,
#             "content": email_content,
#             "sender": step["sender"],
#             "unsubscribe": step["unsubscribe"],
#             "email_signature": step["emailSignature"]
#         }

#         return {
#             "status": "success",
#             "payload": email_payload,
#             "person_id": str(person["_id"]),
#             "public_identifier": person["public_identifier"]
#         }

#     except Exception as e:
#         logger.error(f"Error processing template for {person.get('public_identifier')}: {str(e)}")
#         logger.error(traceback.format_exc())
#         return {
#             "status": "error",
#             "message": f"Error processing template for {person.get('public_identifier')}: {str(e)}"
#         }

def calculate_send_time(base_time: datetime, days: int, time: str, timezone: str, day_type: str) -> datetime:
    tz = pytz.timezone(timezone)
    base_time = base_time.astimezone(tz)
    
    # Parse time
    hour, minute = map(int, time.split(":"))
    
    # Calculate target date
    if day_type == "business_days":
        target_date = add_business_days(base_time, days)
    else:
        target_date = base_time + timedelta(days=days)
    
    # Set the target time
    target_datetime = target_date.replace(hour=hour, minute=minute)
    
    return target_datetime

def add_business_days(date: datetime, days: int) -> datetime:
    current = date
    while days > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            days -= 1
    return current

def populate_template_content(content: str, profile: dict) -> str:
    # Replace variables in content with profile data
    # Add your variable replacement logic here
    return content

def calculate_step_time(step: dict, prev_time: datetime) -> datetime:
    """Calculate the scheduled time for a step based on its configuration."""
    if step["sendingTime"] == "immediate":
        return datetime.utcnow()
    elif step["sendingTime"] == "next_business_day":
        return calculate_next_business_day(prev_time)
    elif step["sendingTime"] == "after":
        return calculate_send_time(
            prev_time,
            step["days"],
            step["time"],
            step["timezone"],
            step["dayType"]
        )
    return prev_time

# Update the AI commands collection schema to be simpler
ai_commands_collection = mongo_database["ai_commands"]

# Example document structure:
# {
#     "_id": ObjectId(),
#     "title": "Work experience",
#     "prompt": "Concise sentence of the candidate's relevant work experience"
# }

@t.get("/ai-commands", response_model=List[dict])
async def get_ai_commands():
    """Fetch all predefined AI commands."""
    try:
        commands = list(ai_commands_collection.find({}, {"title": 1, "prompt": 1}))
        return [to_dict(cmd) for cmd in commands]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Remove create endpoint since we'll manage commands through backend only
