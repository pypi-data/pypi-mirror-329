from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from talentwizer_commons.utils.db import mongo_database

session_router = s = APIRouter()

# MongoDB Setup
collection = mongo_database["session"]

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema):
        json_schema = core_schema
        json_schema.update(type="string")
        return json_schema

class SessionModel(BaseModel):
    # id: str = Field(None, alias="_id")
    id: Optional[PyObjectId] = Field(alias="_id", default_factory=PyObjectId)
    email: str
    mainSession: Optional[dict]
    integrationSession: Optional[dict] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@s.post("/", response_model=SessionModel)
async def create_session(session: SessionModel):
    result = collection.insert_one(session.dict(by_alias=True))
    session.id = str(result.inserted_id)
    return session

@s.get("/{email}", response_model=SessionModel)
async def read_session(email: str):
    session = collection.find_one({"email": email})
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@s.put("/{email}", response_model=SessionModel)
async def update_session(email: str, session: SessionModel):
    session_dict = session.dict(by_alias=True)
    result = collection.update_one({"email": email}, {"$set": session_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@s.delete("/{email}", response_model=SessionModel)
async def delete_session(email: str):
    session = collection.find_one_and_delete({"email": email})
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session