from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
import os
import redis

# Initialize MongoDB connection
client = MongoClient(os.environ["MONGO_URI"])
mongo_database = client[os.environ["MONGODB_DATABASE"]]

def get_sequence_collection():
    """Get the email sequences collection."""
    return mongo_database["email_sequences"]

def get_sequence_audit_collection():
    """Get the email sequence audits collection."""
    return mongo_database["email_sequence_audits"]

def get_mongo_database():
    """Get the MongoDB database instance."""
    return mongo_database

def get_redis_client(decode_responses=True):
    """Get Redis client with proper connection settings"""
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    return redis.Redis.from_url(
        redis_url,
        decode_responses=decode_responses,
        socket_timeout=5,
        socket_connect_timeout=5,
        health_check_interval=30,
        retry_on_timeout=True
    )

# Export the commonly used collections and functions
__all__ = [
    'mongo_database',
    'get_sequence_collection',
    'get_sequence_audit_collection',
    'get_mongo_database'
]