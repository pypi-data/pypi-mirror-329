import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from urllib.parse import unquote
from pydantic import BaseModel, EmailStr
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from msal import ConfidentialClientApplication
import requests
from talentwizer_commons.app.engine import get_chat_engine
from llama_index.core.chat_engine.types import BaseChatEngine
from google.auth.transport.requests import Request
from fastapi import APIRouter, HTTPException, Request, Depends
from dotenv import load_dotenv
from typing import List, Optional
import base64
import os
load_dotenv()
import logging
from datetime import datetime, timedelta
import pytz
from kombu.exceptions import OperationalError
from redis import Redis
import redis
from celery.exceptions import TaskError
from celery.result import AsyncResult
from talentwizer_commons.utils.db import mongo_database
import logging
from .celery_init import celery_app, send_scheduled_email, get_test_delay  # Add get_test_delay here
from .task_status import get_consolidated_task_status, cleanup_completed_tasks  # Add this import
import asyncio
import traceback  # Add at the top with other imports

# Create a Redis connection pool (add after imports)
REDIS_POOL = redis.ConnectionPool.from_url(
    os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    decode_responses=True,
    socket_timeout=5,
    retry_on_timeout=True,
    health_check_interval=30
)

def get_redis_client() -> redis.Redis:
    """Get a Redis client from the connection pool."""
    return redis.Redis(connection_pool=REDIS_POOL)

email_router = e = APIRouter()
logger = logging.getLogger(__name__)

sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

class TokenData(BaseModel):
    accessToken: str
    refreshToken: str
    clientId: str
    clientSecret: str
    idToken: str
    userEmail: str
    scope: str
    authority: Optional[str] = None  # Add this field for Microsoft auth

class EmailPayload(BaseModel):
    from_email: Optional[EmailStr] = None
    to_email: Optional[List[EmailStr]] = None
    cc: Optional[List[EmailStr]] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    attachments: Optional[List[str]] = None

@e.post("/send/admin")    
async def send_email_by_admin_account(emailPayload: EmailPayload):
    from_email = os.getenv("ADMIN_EMAIL")
    if not from_email:
        logging.error("Admin email is not set in environment variables")
        return False

    to_email = emailPayload.to_email
    subject = emailPayload.subject
    body = emailPayload.body
    attachments = emailPayload.attachments

    comma_separated_emails = ",".join(to_email) if to_email else ""
    if not comma_separated_emails:
        logging.error("Recipient email addresses are empty or malformed")
        return False

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = unquote(comma_separated_emails)

    if subject:
        msg['Subject'] = subject
    else:
        logging.warning("Email subject is empty")

    if body:
        msg.attach(MIMEText(body, 'plain'))
    else:
        logging.warning("Email body is empty")

    # Attach files if any
    if attachments:
        for attachment_path in attachments:
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(attachment_path)
                    part.add_header('Content-Disposition', f'attachment; filename={filename}')
                    msg.attach(part)
            except FileNotFoundError:
                logging.error(f"Attachment file not found: {attachment_path}")
            except PermissionError:
                logging.error(f"Permission denied for attachment file: {attachment_path}")
            except Exception as e:
                logging.error(f"Unexpected error attaching file {attachment_path}: {e}")
    
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(from_email, os.getenv("ADMIN_EMAIL_PASSWORD"))
        s.sendmail(from_email, unquote(comma_separated_emails), msg.as_string())
        s.quit()
        logging.info("Email sent successfully through admin email")
        return True
    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP authentication failed. Check ADMIN_EMAIL and ADMIN_EMAIL_PASSWORD")
    except smtplib.SMTPConnectError as e:
        logging.error(f"SMTP connection error: {e}")
    except smtplib.SMTPRecipientsRefused:
        logging.error(f"All recipients were refused: {comma_separated_emails}")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while sending email: {e}")
    return False
        
def create_message(emailPayload: dict, thread_id: str = None):
    """Create email message with proper threading."""
    try:
        logger.info(f"Creating message with thread_id: {thread_id}")
        logger.info(f"Email payload: {emailPayload}")

        # Create base MIME message
        mime_msg = MIMEMultipart('alternative')
        mime_msg['to'] = ', '.join(emailPayload['to_email'])
        mime_msg['from'] = emailPayload.get('sender')
        
        # Add thread headers for follow-up emails
        if thread_id and not emailPayload.get('is_initial'):
            # Use mail.gmail.com format for References/In-Reply-To
            message_id = f"{thread_id}@mail.gmail.com"
            mime_msg['References'] = f"<{message_id}>"
            mime_msg['In-Reply-To'] = f"<{message_id}>"
            # Set Re: subject for follow-ups
            mime_msg['subject'] = f"Re: {emailPayload.get('subject', '')}"
        else:
            mime_msg['subject'] = emailPayload.get('subject', '')

        # Add content
        content = emailPayload.get('content') or emailPayload.get('body')
        html_part = MIMEText(content, 'html', 'utf-8')
        mime_msg.attach(html_part)

        # Convert to Gmail API message format
        message = {
            'raw': base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()
        }

        # Thread ID goes in message body for Gmail API
        if thread_id:
            message['threadId'] = thread_id

        logger.info(f"Created message: {message}")
        return message

    except Exception as e:
        logger.error(f"Error creating message: {str(e)}")
        raise

async def handle_email_reply(thread_id: str, sequence_id: str):
    """Handle a reply received on an email thread"""
    try:
        # Find sequence and update status
        sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
        if not sequence:
            return
            
        # Stop remaining scheduled emails
        audits = sequence_audit_collection.find({
            "sequence_id": sequence_id,
            "status": "SCHEDULED"  
        })
        
        for audit in audits:
            if audit.get("schedule_id"):
                # Cancel scheduled task
                task = AsyncResult(audit["schedule_id"])
                task.revoke(terminate=True)
                
            # Update audit status
            sequence_audit_collection.update_one(
                {"_id": audit["_id"]},
                {"$set": {
                    "status": "CANCELLED",
                    "updated_at": datetime.utcnow(),
                    "cancel_reason": "User replied to thread"
                }}
            )
            
        # Update sequence status
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {"$set": {
                "status": "COMPLETED",
                "updated_at": datetime.utcnow(),
                "completion_reason": "User replied to thread"
            }}
        )
        
    except Exception as e:
        logger.error(f"Error handling email reply: {str(e)}")
        raise

async def handle_unsubscribe(sequence_id: str):
    """Handle unsubscribe request for a sequence"""
    try:
        # Similar to handle_email_reply but with different status reason
        # ...implement unsubscribe logic...
        pass
    except Exception as e:
        logger.error(f"Error handling unsubscribe: {str(e)}")
        raise

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        logging.info('Message Id: %s' % message['id'])
        logging.info('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        logging.error('An error occurred: %s' % error)
        return None

def send_message_gmail(service, user_id, message, thread_id=None):
    """Send an email via Gmail API with proper thread handling."""
    try:
        # Create API request - threadId should be part of message body, not params
        if thread_id:
            message['threadId'] = thread_id  # Add threadId to message body
            logger.info(f"Added threadId to message body: {thread_id}")

        request = service.users().messages().send(
            userId=user_id,
            body=message
        )
        
        response = request.execute()
        thread_id = response.get('threadId')
        logger.info(f"Gmail API response threadId: {thread_id}")

        return {
            "status_code": 200,
            "message": "Email sent successfully", 
            "threadId": thread_id
        }

    except Exception as e:
        logger.error(f"Error sending Gmail message: {str(e)}")
        raise

def send_message_microsoft(access_token: str, payload: EmailPayload, thread_id: str = None):
    """Send an email via Microsoft Graph API with proper thread handling."""
    try:
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Convert EmailPayload to Microsoft Graph API format
        message = {
            "message": {
                "subject": payload.subject if not thread_id else None,  # Only set subject for new threads
                "body": {
                    "contentType": "HTML",
                    "content": payload.body
                },
                "toRecipients": [{"emailAddress": {"address": email}} for email in payload.to_email],
                "ccRecipients": [{"emailAddress": {"address": email}} for email in (payload.cc or [])]
            },
            "saveToSentItems": "true"
        }

        # Add thread context if replying
        if thread_id:
            message["message"]["conversationId"] = thread_id
            message["message"]["replyTo"] = [{"emailAddress": {"address": payload.from_email}}]

        # Add attachments if any
        if payload.attachments:
            message["message"]["attachments"] = [
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": os.path.basename(attachment),
                    "contentBytes": base64.b64encode(open(attachment, "rb").read()).decode()
                }
                for attachment in payload.attachments
            ]

        response = requests.post(url, headers=headers, json=message)
        
        if response.status_code not in (200, 202):
            raise RuntimeError(f"Error sending email via Microsoft Graph API: {response.text}")

        # Get thread ID from response headers or response body
        thread_id = (
            response.headers.get("conversationId") or
            response.json().get("conversationId") or
            thread_id
        )

        return {
            "status_code": response.status_code,
            "threadId": thread_id,
            "message": "Email sent successfully via Microsoft"
        }

    except Exception as e:
        logger.error(f"Microsoft Graph API error: {str(e)}")
        raise

def build_gmail_service(token_data: dict):
    """Build Gmail API service with credentials from token data."""
    try:
        creds = Credentials(
            token=token_data["accessToken"],
            refresh_token=token_data["refreshToken"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=token_data["clientId"],
            client_secret=token_data["clientSecret"],
            scopes=token_data["scope"].split()
        )
        
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        logger.error(f"Error building Gmail service: {str(e)}")
        raise RuntimeError(f"Failed to build Gmail service: {str(e)}")

async def send_email_from_user_email(tokenData: dict, emailPayload: EmailPayload, thread_id: str = None):
    """Send email with proper threading support."""
    try:
        # Convert EmailPayload to dict and add thread info
        payload_dict = emailPayload.dict()
        payload_dict['is_reply'] = bool(thread_id)  # Mark as reply if thread_id exists
        
        # Create message with thread info
        message = create_message(payload_dict, thread_id)
        
        if "gmail.send" in tokenData.get("scope", ""):
            gmail_service = build_gmail_service(tokenData)
            response = send_message_gmail(gmail_service, 'me', message, thread_id)
        else:
            response = send_message_microsoft(tokenData["accessToken"], emailPayload, thread_id)
            
        return response
        
    except Exception as e:
        logger.error("Error sending email", exc_info=True)
        raise RuntimeError(f"Error sending email: {str(e)}")

@e.get("/generate")
async def generate_personalised_email(
    company_name:str,
    person_name: str,
    person_summary: str,
    title: str,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
):
    prompt = "You are an expert recruiter and co-pilot for recruitment industry. "
    prompt += "Help generate a Email based on Job Title, Person Summary and Person Name to be sent to the potential candidate. " 
    prompt+= "Company Name: " + company_name +"\n"
    
    if(person_name!=""):
      prompt += "Person Name: " + str(person_name) + "\n"
      
    prompt += "Person Summary:" + str(person_summary) + "\n"
    prompt += "Job Title:" + str(title) + "\n"
    
    prompt += "Try to Write like this: Hi Based on your description your profile is being shortlisted/rejeected etc. Try to Write in about 150 words. Do not Add Any Types Of Salutations. At Ending Just Write Recruiting Team and There Company Name"
    response=chat_engine.chat(prompt)
    return response.response


@e.get("/generate/summary")
async def generate_summary(
    job_title: str,
    person_summary: str
):
    chat_engine: Optional[BaseChatEngine] = None
    try:
        # Validate inputs
        if not job_title.strip():
            raise ValueError("Job title cannot be empty.")
        if not person_summary.strip():
            raise ValueError("Person summary cannot be empty.")

        # Prepare the prompt
        prompt = (
            "You are an expert recruiter and co-pilot for the recruitment industry. "
            f"Job Title: {job_title}\n"
            f"Person Summary: {person_summary}\n"
            "Summarise person's experience and expertise based on the given Person Summary "
            "in the context of an interview mail. Personalise the content as if you are "
            "writing an email or talking to the candidate directly to show him/her as the best fit for the job. \n"
            "The email should be concise and engaging.\n"
            "Example:  based on your experience and expertise, you are a perfect fit for the job. "
            "Do not write full email content but just a summary of the candidate's experience with "
            "regard to the given job title. Try to summarise in about 50 to 60 words."
        )

        # Resolve chat_engine if not provided
        if chat_engine is None:
            chat_engine = get_chat_engine()

        # Call the chat engine
        response = chat_engine.chat(prompt)
        
        # Ensure the response is valid
        if not response or not hasattr(response, "response"):
            raise ValueError("Chat engine did not return a valid response.")

        return response.response

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the summary.")


# Utility function to replace placeholders in the email template
async def populate_template_v1(template: str, person: dict, job_title: str) -> str:
    """
    Populates a template with data from the provided person and job title. 

    Args:
        template: The template string with placeholders.
        person: A dictionary containing information about the person.
        job_title: The target job title.

    Returns:
        The populated template string.

    Raises:
        ValueError: If the input parameters are invalid.
        HTTPException: If an error occurs during template population.
    """

    try:
        # Validate inputs
        if not isinstance(template, str) or not template.strip():
            raise ValueError("Template must be a non-empty string.")
        if not isinstance(person, dict):
            raise ValueError("Person must be a dictionary.")
        if not isinstance(job_title, str) or not job_title.strip():
            raise ValueError("Job title must be a non-empty string.")

        # Generate the brief summary
        brief_summary: Optional[str] = await generate_summary(job_title, person.get("summary", ""))

        if not brief_summary:
            raise ValueError("Failed to generate a brief summary for the candidate.")

        # Replace placeholders conditionally
        populated_template = template

        if "{{First Name}}" in template:
            populated_template = populated_template.replace("{{First Name}}", person.get("name", "Candidate"))

        if "{{Current Company}}" in template:
            populated_template = populated_template.replace("{{Current Company}}", person.get("work_experience", [{}])[0].get("company_name", "Company")) 

        if "{{Current Job Title}}" in template:
            # populated_template = populated_template.replace("{{Current Job Title}}", person.get("occupation", "Job Title"))
             populated_template = populated_template.replace("{{Current Job Title}}", person.get("work_experience", [{}])[0].get("designation", "Job Title")) 
        if "{*Brief mention of the candidate’s relevant skills.*}" in template:
            populated_template = populated_template.replace("{*Brief mention of the candidate’s relevant skills.*}", brief_summary)

        return populated_template

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while populating the template.")

async def populate_template_v2(template: str, person: dict, job_title: str) -> str:
    try:
        # Better validation with helpful error messages
        if not template:
            return ""  # Return empty string instead of raising error for empty template
            
        if not isinstance(person, dict):
            raise ValueError("Person data must be a dictionary")
            
        if not job_title:
            raise ValueError("Job title cannot be empty")

        # Fetch values with defaults
        full_name = person.get("full_name", "Candidate")
        current_company = person.get("experience", [{}])[0].get("company_name", "Company")
        person_job_title = person.get("experience", [{}])[0].get("title", "Title")
        summary = person.get("summary", "skills and experience")

        # Generate the brief summary
        brief_summary: Optional[str] = await generate_summary(job_title, summary)

        if not brief_summary:
            raise ValueError("Failed to generate a brief summary for the candidate.")

        # Replace placeholders in the template
        populated_template = (
            template.replace("{{Full Name}}", full_name)
            .replace("{{Current Company}}", current_company)
            .replace("{{Current Job Title}}", person_job_title)
            .replace("{{Client Company}}", "our company")
            .replace("{*Brief mention of the candidate’s relevant skills.*}", brief_summary)
            .replace("{{Client Job Title}}", job_title)
        )

        return populated_template

    except ValueError as ve:
        logger.error(f"Template population error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in template population: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error populating template: {str(e)}")
    
async def send_failure_report(reports: List[dict]):
    try:
        for report in reports:
            report_payload = EmailPayload(
                to_email=[report["to_email"]],
                subject=report["subject"],
                body=report["body"]
            )
            await send_email_by_admin_account(report_payload)
    except Exception as e:
        logging.error("Failed to send failure report emails", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to send failure report emails: {str(e)}")


send_email_task = send_scheduled_email

async def check_redis_queue(redis_instance: redis.Redis, key: str, task_id: str) -> bool:
    """Safely check Redis queue existence and type."""
    try:
        # Check if key exists and is the right type
        key_type = redis_instance.type(key)
        if key_type == b'zset':
            return redis_instance.zscore(key, task_id) is not None
        elif key_type == b'none':
            # Initialize as sorted set if doesn't exist
            redis_instance.zadd(key, {task_id: float(datetime.now().timestamp())})
            return True
        else:
            # Wrong type, reinitialize
            redis_instance.delete(key)
            redis_instance.zadd(key, {task_id: float(datetime.now().timestamp())})
            return True
    except Exception as e:
        logger.error(f"Redis operation failed for key {key}: {str(e)}")
        return False

async def schedule_email(email_payload: dict, scheduled_time: datetime = None, timezone: str = None, token_data: dict = None) -> str:
    """Schedule an email to be sent at a specific time."""
    redis_instance = None
    try:
        # Get Redis client from pool
        redis_instance = get_redis_client()
        
        # Test connection
        if not redis_instance.ping():
            raise ConnectionError("Could not connect to Redis")

        # Convert EmailPayload to dict if it's a Pydantic model
        if isinstance(email_payload, EmailPayload):
            email_payload = email_payload.dict()
            
        # Fix email payload issue - move content to body
        if 'content' in email_payload and 'body' not in email_payload:
            email_payload['body'] = email_payload.pop('content')
            
        # Check test mode first
        test_delay = get_test_delay()
        if test_delay and not scheduled_time:
            # Extract just the base_delay value for the first email
            base_delay = test_delay.get('base_delay', 60)  # Default 60 seconds
            logger.info(f"Test mode enabled, using {base_delay} seconds base delay")
            scheduled_time = datetime.utcnow() + timedelta(seconds=base_delay)
            logger.info(f"Overriding scheduled time to: {scheduled_time}")

        logger.info(f"Final scheduling time: {scheduled_time}")
        logger.info(f"Email payload: {email_payload}")
        
        # Schedule task with token data
        task = send_email_task.apply_async(
            kwargs={
                'email_payload': email_payload,
                'scheduled_time': scheduled_time.isoformat() if scheduled_time else None,
                'token_data': token_data
            },
            eta=scheduled_time,
            queue='email_queue',
            routing_key='email.send'
        )
        
        logger.info(f"Task scheduled with ID: {task.id}")
        
        # Just verify task in Redis and return ID
        max_attempts = 5
        for attempt in range(max_attempts):
            if await check_redis_queue(redis_instance, 'unacked', task.id) or \
               await check_redis_queue(redis_instance, 'reserved', task.id):
                logger.info(f"Task {task.id} verified in Redis")
                return str(task.id)
            
            logger.warning(f"Task not found in Redis, attempt {attempt + 1}/{max_attempts}")
            await asyncio.sleep(0.5)
            
        raise Exception("Task was not properly scheduled in Redis")

    except Exception as e:
        logger.error(f"Failed to schedule email: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up Redis connection if needed
        if redis_instance:
            try:
                redis_instance.close()
            except:
                pass

@e.get("/scheduled-email/{task_id}")
async def check_scheduled_email(task_id: str):
    """Check the status of a scheduled email task."""
    try:
        result = AsyncResult(task_id, app=celery_app)
        return {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check task status: {str(e)}")

@e.get("/scheduled-emails")
async def list_scheduled_emails():
    """List all scheduled email tasks in Redis."""
    try:
        redis_client = redis.Redis.from_url(os.getenv('CELERY_BROKER_URL'))
        scheduled_tasks = redis_client.zrange('unacked', 0, -1)
        return {
            "scheduled_tasks": [task.decode() for task in scheduled_tasks]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list scheduled tasks: {str(e)}")

# @e.post("/schedule-email")
# async def schedule_email(email_payload: EmailPayload, delay: int, timezone: str, time: str, days: int, day_type: str):
#     # Calculate the delay based on the provided details
#     user_timezone = pytz.timezone(timezone)
#     now = datetime.now(user_timezone)
#     scheduled_time = datetime.strptime(time, "%H:%M").time()
#     scheduled_datetime = datetime.combine(now, scheduled_time)

#     if day_type == "business_days":
#         business_days_to_add = days
#         current_day = now.weekday()
#         days_to_add = (business_days_to_add - (4 - current_day)) % 5
#         if days_to_add <= 0:
#             days_to_add += 5
#         scheduled_datetime += timedelta(days=days_to_add)
#     else:
#         scheduled_datetime += timedelta(days=days)

#     delay_seconds = (scheduled_datetime - now).total_seconds()
#     if delay_seconds < 0:
#         delay_seconds = 0

#     send_email_task.apply_async(args=[email_payload.dict(), int(delay_seconds)], countdown=int(delay_seconds))
#     return {"message": "Email scheduled successfully"}

async def refresh_token(token_data: dict) -> dict:
    """Refresh the access token using the refresh token."""
    try:
        if "https://www.googleapis.com/auth/gmail.send" in token_data.get("scope", ""):
            # Refresh Gmail token
            creds = Credentials(
                token=token_data["accessToken"],
                refresh_token=token_data["refreshToken"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=token_data["clientId"],
                client_secret=token_data["clientSecret"],
                scopes=token_data["scope"].split()
            )
            creds.refresh(Request())
            return {
                **token_data,
                "accessToken": creds.token,
                "refreshToken": creds.refresh_token
            }
        elif "Mail.Send" in token_data.get("scope", ""):
            # Refresh Microsoft token
            app = ConfidentialClientApplication(
                token_data["clientId"],
                authority=token_data.get("authority", "https://login.microsoftonline.com/common"),
                client_credential=token_data["clientSecret"]
            )
            result = app.acquire_token_by_refresh_token(
                token_data["refreshToken"],
                scopes=["Mail.Send"]
            )
            if "access_token" not in result:
                raise Exception("Failed to refresh token")
            return {
                **token_data,
                "accessToken": result["access_token"]
            }
    except Exception as e:
        logging.error(f"Error refreshing token: {str(e)}")
        raise

@celery_app.task
def send_email_with_retry(email_payload: dict, token_data: dict, max_retries: int = 3):
    """Send email with token refresh retry logic."""
    try:
        # Get thread_id from payload
        thread_id = email_payload.get('thread_id')
        
        # Convert dict back to EmailPayload
        payload = EmailPayload(**email_payload)
        
        # Send email with thread_id
        result = send_email_from_user_email(token_data, payload, thread_id)
        
        if result["status_code"] == 200:
            # Use existing thread_id if available, otherwise get new one
            response_thread_id = result.get('threadId') or thread_id
            
            if response_thread_id:
                # Update sequence audit with thread ID
                sequence_audit_collection.update_many(
                    {"sequence_id": email_payload.get("sequence_id")},
                    {"$set": {"thread_id": response_thread_id}}
                )
            
            return result
            
    except Exception as e:
        logger.error(f"Error in send_email_with_retry: {str(e)}")
        raise

@e.get("/scheduled-tasks/stats")
async def get_scheduled_tasks_stats():
    """Get statistics about scheduled tasks."""
    stats = {
        "redis": {"status": "unknown"},
        "celery": {"status": "unknown"},
        "database": {"status": "unknown"}
    }

    try:
        # Redis checks with connection pooling and error handling
        try:
            redis_pool = redis.ConnectionPool.from_url(
                os.getenv('CELERY_BROKER_URL'),
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30,
                max_connections=10
            )
            
            redis_client = redis.Redis(connection_pool=redis_pool)
            redis_client.ping()  # Test connection
            
            stats["redis"] = {
                "status": "connected",
                "unacked": redis_client.zcard('unacked'),
                "scheduled": redis_client.zcard('scheduled'),
                "queue_length": redis_client.llen('celery')
            }
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {str(e)}")
            stats["redis"].update({
                "status": "disconnected",
                "error": str(e)
            })
        finally:
            if 'redis_pool' in locals():
                redis_pool.disconnect()

        # Celery checks with timeout
        try:
            # Only use supported timeout parameter
            inspector = celery_app.control.inspect(timeout=3.0)
            
            # Check worker availability
            if not inspector.ping():
                raise ConnectionError("No Celery workers responded to ping")
            
            active = inspector.active() or {}
            scheduled = inspector.scheduled() or {}
            reserved = inspector.reserved() or {}
            
            stats["celery"] = {
                "status": "connected",
                "active": sum(len(tasks) for tasks in active.values()),
                "reserved": sum(len(tasks) for tasks in reserved.values()),
                "scheduled": sum(len(tasks) for tasks in scheduled.values())
            }
        except (ConnectionError, TimeoutError, OSError) as e:
            logger.error(f"Celery inspection error: {str(e)}")
            stats["celery"].update({
                "status": "disconnected",
                "error": str(e)
            })

        # Database checks with error handling
        try:
            pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
            audit_counts = list(sequence_audit_collection.aggregate(pipeline))
            
            stats["database"] = {
                "status": "connected",
                "audit_counts": audit_counts
            }
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            stats["database"].update({
                "status": "error",
                "error": str(e)
            })

        return stats

    except Exception as e:
        logger.error(f"Failed to get task stats: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "component_status": {
                "redis": stats["redis"]["status"],
                "celery": stats["celery"]["status"],
                "database": stats["database"]["status"]
            }
        }

@e.get("/scheduled-tasks/details")
async def list_scheduled_task_details():
    """List all scheduled tasks with their details."""
    try:
        redis_client = redis.Redis.from_url(os.getenv('CELERY_BROKER_URL'))
        scheduled_tasks = []
        
        # Get tasks from Redis
        tasks = redis_client.zrange('unacked', 0, -1, withscores=True)
        
        for task_id, score in tasks:
            try:
                task_id_str = task_id.decode()
                task = AsyncResult(task_id_str, app=celery_app)
                scheduled_time = datetime.fromtimestamp(score)
                
                # Get task info from audit collection
                audit = sequence_audit_collection.find_one({"schedule_id": task_id_str})
                
                if audit:
                    task_info = {
                        "task_id": task_id_str,
                        "status": task.status,
                        "scheduled_time": scheduled_time.isoformat(),
                        "recipient": audit["email_payload"]["to_email"] if audit.get("email_payload") else None,
                        "subject": audit["email_payload"]["subject"] if audit.get("email_payload") else None,
                        "sequence_id": audit.get("sequence_id"),
                        "error": audit.get("error_message"),
                        "sent_time": audit.get("sent_time", "").isoformat() if audit.get("sent_time") else None
                    }
                    scheduled_tasks.append(task_info)
            except Exception as task_error:
                logger.error(f"Error processing task {task_id}: {str(task_error)}", exc_info=True)
                continue
        
        return {
            "scheduled_tasks": scheduled_tasks,
            "total_count": len(scheduled_tasks)
        }
    except Exception as e:
        logger.error(f"Failed to list scheduled tasks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list scheduled tasks: {str(e)}")

@e.delete("/scheduled-tasks/{task_id}")
async def cancel_scheduled_task(task_id: str):
    """Cancel a scheduled task."""
    try:
        # Get task from Celery
        task = AsyncResult(task_id, app=celery_app)
        task.revoke(terminate=True)
        
        # Remove from Redis if present
        redis_client = redis.Redis.from_url(os.getenv('CELERY_BROKER_URL'))
        redis_client.zrem('unacked', task_id.encode())
        
        # Update audit record
        result = sequence_audit_collection.update_one(
            {"schedule_id": task_id},
            {
                "$set": {
                    "status": "CANCELLED",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found in audit collection")
        
        return {
            "message": f"Task {task_id} cancelled successfully",
            "status": "CANCELLED"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Failed to cancel task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to cancel task: {str(e)}")

def get_formatted_times(scheduled_time: str | datetime | int | float) -> dict:
    """Convert various time formats to UTC and IST timezones."""
    try:
        # Handle different input types
        if isinstance(scheduled_time, datetime):
            utc_time = scheduled_time.astimezone(pytz.UTC)
        else:
            # Convert to string for consistent handling
            scheduled_time_str = str(scheduled_time)

            try:
                # Try parsing numeric timestamp
                if scheduled_time_str.isdigit() or scheduled_time_str.replace('.', '').isdigit():
                    utc_time = datetime.fromtimestamp(float(scheduled_time_str), tz=pytz.UTC)
                # Try parsing ISO format
                else:
                    # Clean up the time string
                    clean_time = scheduled_time_str.strip()
                    # Remove any trailing Z and replace with proper UTC offset
                    if clean_time.endswith('Z'):
                        clean_time = clean_time[:-1] + '+00:00'
                    # Add UTC offset if missing
                    elif not any(x in clean_time for x in ['+', '-', 'Z']):
                        clean_time += '+00:00'
                    utc_time = datetime.fromisoformat(clean_time)
                    if utc_time.tzinfo is None:
                        utc_time = pytz.UTC.localize(utc_time)
            except (ValueError, TypeError):
                # If all else fails, try dateutil parser
                from dateutil import parser
                utc_time = parser.parse(scheduled_time_str)
                if utc_time.tzinfo is None:
                    utc_time = pytz.UTC.localize(utc_time)

        # Convert to IST
        ist = pytz.timezone('Asia/Kolkata')
        ist_time = utc_time.astimezone(ist)
        
        return {
            'utc': utc_time.strftime('%Y-%m-%d %I:%M:%S %p UTC'),
            'ist': ist_time.strftime('%Y-%m-%d %I:%M:%S %p IST'),
            'timestamp': int(utc_time.timestamp())
        }
    except Exception as e:
        logger.error(f"Error formatting time {scheduled_time}: {str(e)}", exc_info=True)
        return {
            'utc': str(scheduled_time),
            'ist': 'Invalid date format',
            'timestamp': None
        }

@e.get("/scheduled-tasks/monitor")
async def monitor_scheduled_tasks(include_completed: bool = False):
    """Get comprehensive task monitoring information."""
    try:
        # Run cleanup synchronously since it's not an async function
        cleanup_completed_tasks()
        
        # Get consolidated status, excluding completed tasks by default
        status = get_consolidated_task_status(24, include_completed=False)
        
        # Add formatted times for better readability
        for task in status.get("tasks", []):
            if task.get("scheduled_time"):
                task["formatted_times"] = get_formatted_times(task["scheduled_time"])
                
            # Add additional task details
            if task.get("task_id"):
                celery_task = AsyncResult(task["task_id"], app=celery_app)
                task["celery_status"] = celery_task.status
                if celery_task.result:
                    task["celery_result"] = str(celery_task.result)

        # Add system health indicators
        status["system_health"] = {
            "redis": status["redis_status"] == "connected",
            "celery": status["celery_status"] == "connected",
            "database": status["db_status"] == "connected",
            "overall": all(x == "connected" for x in [
                status["redis_status"],
                status["celery_status"],
                status["db_status"]
            ])
        }
        
        return {
            "status": "success",
            "data": status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Monitor error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error getting task status",
                "error": str(e)
            }
        )

async def get_redis_tasks(redis_client):
    """Get task information from Redis."""
    tasks = []
    try:
        for key in ['unacked', 'scheduled', 'reserved']:
            items = redis_client.zrange(key, 0, -1, withscores=True)
            tasks.extend([{
                "id": item[0],
                "score": item[1],
                "queue": key
            } for item in items])
    except Exception as e:
        logger.error(f"Error getting Redis tasks: {str(e)}")
    return tasks

async def get_task_info(task):
    """Get detailed task information."""
    try:
        task_id = task.get("schedule_id")
        if not task_id:
            return None

        celery_task = AsyncResult(task_id, app=celery_app)
        
        return {
            "task_id": task_id,
            "status": celery_task.status,
            "scheduled_time": task.get("scheduled_time"),
            "email_payload": task.get("email_payload"),
            "token_data_present": bool(task.get("token_data")),
            "token_data": {  # Add redacted token info
                "provider": "gmail" if "gmail.send" in task.get("token_data", {}).get("scope", "") else "microsoft",
                "user_email": task.get("token_data", {}).get("userEmail"),
                "has_refresh_token": bool(task.get("token_data", {}).get("refreshToken"))
            } if task.get("token_data") else None,
            "created_at": task.get("created_at"),
            "celery_info": celery_task.info,
            "test_mode": bool(os.getenv('TEST_MODE') == 'true')
        }
    except Exception as e:
        logger.error(f"Error getting task info: {str(e)}")
        return None

async def process_ai_commands(commands: List[str], profile: dict, chat_engine: BaseChatEngine) -> str:
    """Process AI smart commands to generate personalized content."""
    results = []
    for command in commands:
        prompt = f"""
        As a recruiting expert, analyze this candidate profile and {command}
        Profile: {profile}
        
        Provide a brief, natural response that can be included in an email.
        """
        response = await chat_engine.chat(prompt)
        results.append(response.response)
    
    return " ".join(results)

def add_unsubscribe_link(body: str, sequence_id: str, profile_id: str) -> str:
    """Add unsubscribe link to email body."""
    unsubscribe_url = f"{os.getenv('PUBLIC_API_URL')}/unsubscribe?sequence_id={sequence_id}&profile_id={profile_id}"
    unsubscribe_html = f"""
    <br><br>
    <div style="color: #666; font-size: 12px; margin-top: 20px;">
        <p>To unsubscribe from this email sequence, <a href="{unsubscribe_url}">click here</a></p>
    </div>
    """
    return body + unsubscribe_html

async def process_sequence_for_person(person: dict, template: dict, step: dict, job_title: str, chat_engine: BaseChatEngine = None) -> dict:
    """Process a template sequence step for a person."""
    try:
        # Validate inputs
        if not step:
            raise ValueError("Step data is required")

        # Get primary email
        email = person.get("email", [])
        if isinstance(email, list):
            email = email[0] if email else None
        
        if not email:
            return {
                "status": "error",
                "message": f"No email found for profile {person.get('public_identifier')}"
            }

        # Process AI commands first
        ai_content = ""
        if step.get("aiCommands"):
            if not chat_engine:
                chat_engine = get_chat_engine()
            ai_content = await process_ai_commands(step["aiCommands"], person, chat_engine)

        # Replace variables in template content
        email_content = await populate_template_v2(step.get("content", ""), person, job_title) or ""
        
        # Only populate subject for initial email
        subject = None
        if step.get("is_initial"):
            subject = await populate_template_v2(step.get("subject", ""), person, job_title) or ""
            if not subject.strip():
                raise ValueError("Subject is required for initial email")
        
        # Add AI-generated content if any
        if ai_content:
            email_content += f"\n\n{ai_content}"
            
        # Add unsubscribe link if enabled
        if step.get("unsubscribe"):
            email_content = add_unsubscribe_link(
                email_content, 
                str(step.get("sequence_id")), 
                str(person.get("_id"))
            )

        email_payload = {
            "to_email": [email],
            "subject": subject,
            "content": email_content,
            "sender": step.get("sender"),
            "unsubscribe": step.get("unsubscribe", False),
            "email_signature": step.get("emailSignature", "")
        }

        return {
            "status": "success",
            "payload": email_payload,
            "person_id": str(person.get("_id")),
            "public_identifier": person.get("public_identifier")
        }

    except ValueError as ve:
        logger.error(f"Error processing template for {person.get('public_identifier')}: {str(ve)}")
        return {
            "status": "error",
            "message": str(ve)
        }
    except Exception as e:
        logger.error(f"Unexpected error processing template: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

async def check_for_replies(service, thread_id: str, sender_email: str) -> bool:
    """Check if there are any replies in the thread from anyone other than the sender."""
    try:
        thread = service.users().threads().get(
            userId='me',
            id=thread_id,
            format='metadata',
            metadataHeaders=['From', 'To', 'Message-ID', 'In-Reply-To', 'References']
        ).execute()

        if not thread.get('messages'):
            return False

        messages = sorted(thread['messages'], key=lambda x: int(x['internalDate']))
        
        # Get initial message details
        initial_msg = messages[0]
        initial_headers = {
            h['name'].lower(): h['value'].lower() 
            for h in initial_msg['payload']['headers']
        }
        
        initial_message_id = initial_headers.get('message-id', '')
        sender_email = sender_email.lower()
        
        logger.info(f"Thread {thread_id} - Initial Message-ID: {initial_message_id}")
        logger.info(f"Checking for replies not from: {sender_email}")

        # Check each subsequent message
        for msg in messages[1:]:
            headers = {
                h['name'].lower(): h['value'].lower() 
                for h in msg['payload']['headers']
            }
            
            from_email = headers.get('from', '').lower()
            refs = headers.get('references', '').lower()
            reply_to = headers.get('in-reply-to', '').lower()
            
            logger.info(f"Checking message - From: {from_email}")
            logger.info(f"References: {refs}, In-Reply-To: {reply_to}")

            # Message is a reply if either:
            # 1. It references the initial message
            # 2. It's in-reply-to the initial message
            is_reply = (initial_message_id in refs) or (initial_message_id == reply_to)
            
            # And it's from someone other than the sender
            if is_reply and sender_email not in from_email:
                logger.info(f"Reply detected from {from_email}")
                return True

        logger.info("No external replies found")
        return False

    except Exception as e:
        logger.error(f"Error checking replies: {str(e)}", exc_info=True)
        return False

async def check_outlook_replies(access_token: str, thread_id: str, sender_email: str) -> bool:
    """Check for replies in Outlook thread."""
    try:
        url = f"https://graph.microsoft.com/v1.0/me/messages/{thread_id}/replies"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            replies = response.json().get('value', [])
            return any(reply['from']['emailAddress']['address'] != sender_email for reply in replies)
        return False
        
    except Exception as e:
        logger.error(f"Error checking Outlook replies: {str(e)}")
        return False

@celery_app.task
def send_email_with_retry(email_payload: dict, token_data: dict, max_retries: int = 3):
    """Send email with token refresh retry logic."""
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                # Refresh token before retrying
                token_data = refresh_token(token_data)
            
            # Convert dict back to EmailPayload before sending
            payload = EmailPayload(**email_payload)
            
            # Check for existing thread_id
            thread_id = email_payload.get('thread_id')
            
            # Send email and get thread ID
            result = send_email_from_user_email(token_data, payload, thread_id)
            
            if result["status_code"] == 200:
                # Store thread_id for future steps
                if result.get("threadId"):
                    sequence_audit_collection.update_one(
                        {"_id": email_payload.get("audit_id")},
                        {"$set": {"thread_id": result["threadId"]}}
                    )
                return result
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logging.warning(f"Email send attempt {attempt + 1} failed, retrying...")
            continue

async def process_sequence_step(step: dict, person: dict, template: dict, thread_id: str = None):
    """Process a single sequence step, checking for replies before sending."""
    try:
        # Check for replies before sending follow-up
        if thread_id:
            has_reply = False
            if "gmail.send" in step["token_data"].get("scope", ""):
                gmail_service = build('gmail', 'v1', credentials=step["token_data"])
                has_reply = await check_for_replies(gmail_service, thread_id, step["sender"])
            elif "Mail.Send" in step["token_data"].get("scope", ""):
                has_reply = await check_outlook_replies(
                    step["token_data"]["accessToken"],
                    thread_id,
                    step["sender"]
                )
                
            if has_reply:
                # Update sequence status and cancel remaining steps
                await handle_email_reply(thread_id, str(step["sequence_id"]))
                return {
                    "status": "cancelled",
                    "message": "Sequence cancelled due to recipient reply"
                }
                
        # Process and send email
        email_result = await process_sequence_for_person(person, template, step)
        if email_result["status"] == "success":
            email_payload = {
                **email_result["payload"],
                "thread_id": thread_id,
                "audit_id": step.get("audit_id")
            }
            
            return await schedule_email(
                email_payload=email_payload,
                scheduled_time=step.get("scheduled_time"),
                token_data=step["token_data"]
            )
            
        return email_result
        
    except Exception as e:
        logger.error(f"Error processing sequence step: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

# ... rest of existing code remains unchanged ...