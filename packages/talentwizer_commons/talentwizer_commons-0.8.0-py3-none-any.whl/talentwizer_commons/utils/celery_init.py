import os
from celery import Celery, signals
from celery.states import PENDING, SUCCESS, FAILURE  # Add this import
from kombu import Queue, Exchange
import redis
import logging
from datetime import datetime, timedelta
import json
import asyncio
from bson import ObjectId
from celery.signals import worker_ready, after_setup_logger, after_setup_task_logger, celeryd_after_setup, task_sent, task_received, task_success, task_failure
from celery.schedules import crontab
import threading
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)

# Add JSON encoder class
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Initialize MongoDB collections
from talentwizer_commons.utils.db import mongo_database
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

def get_redis_url():
    """Get properly formatted Redis URL with separate DB for Celery"""
    # Use localhost with explicit port
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_db = os.getenv('CELERY_REDIS_DB', '0')
    
    # Always return a fully formatted URL
    return f"redis://{redis_host}:{redis_port}/{redis_db}"

# Add this before creating celery_app
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
os.environ['FORKED_BY_MULTIPROCESSING'] = '1'

# Create the Celery application with proper name and imports
celery_app = Celery(
    'talentwizer_commons',
    broker=get_redis_url(),
    backend=get_redis_url(),
    include=['talentwizer_commons.utils.celery_init']
)

# Update Celery configuration (remove duplicate entries)
celery_app.conf.update(
    # Broker settings
    broker_transport_options={
        'visibility_timeout': 43200,
        'fanout_prefix': True,
        'fanout_patterns': True,
        'global_keyprefix': 'celery:',
        'broker_connection_retry': True,
        'broker_connection_max_retries': None,
        'result_backend_transport_options': {
            'visibility_timeout': 43200,
            'retry_policy': {
                'timeout': 5.0
            }
        }
    },
    broker_connection_retry_on_startup=True,
    broker_pool_limit=None,
    broker_connection_timeout=5,
    
    # Task settings
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    task_track_started=True,
    task_ignore_result=False,
    task_store_errors_even_if_ignored=True,
    result_expires=None,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=600,
    task_soft_time_limit=300,
    task_send_sent_event=True,
    task_default_rate_limit='100/m',
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_lost_wait=30,
    worker_max_tasks_per_child=1000,
    worker_max_memory_per_child=150000,
    worker_state_db='/tmp/celery/worker.state',
    worker_state_persistent=True,
    worker_send_task_events=True,
    
    # Queue configuration
    task_queues=(
        Queue('celery', Exchange('celery'), routing_key='celery'),
        Queue('email_queue', Exchange('email_queue', type='direct'), routing_key='email.#'),
    ),
    
    # Task routing
    task_routes={
        'send_scheduled_email': {
            'queue': 'email_queue',
            'routing_key': 'email.send'
        },
        'restore_persisted_tasks': {
            'queue': 'celery',
            'routing_key': 'celery'
        }
    },
    
    # Worker pool settings
    worker_pool='threads',  # Use threads instead of processes
    worker_pool_restarts=True,
)

# Update Redis initialization
def init_redis_queues():
    """Initialize Redis queues with proper formats."""
    try:
        redis_client = redis.Redis.from_url(
            get_redis_url(),
            decode_responses=True,
            socket_timeout=5,
            retry_on_timeout=True
        )
        
        # Clear old keys if needed
        old_keys = ['unacked', 'reserved', 'scheduled']
        for key in old_keys:
            if redis_client.exists(key):
                redis_client.delete(key)
        
        # Initialize new keys with proper prefix and type
        redis_client.zadd('celery:unacked', {})
        redis_client.zadd('celery:reserved', {})
        redis_client.zadd('celery:scheduled', {})
        
        logger.info("Redis queues initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Redis queues: {str(e)}")
        raise

# Move initialization to a function that can be called explicitly
def initialize():
    """Initialize Celery and Redis configurations"""
    init_redis_queues()

def get_test_delay():
    """Get delay time based on environment"""
    if os.getenv('TEST_MODE') == 'true':
        base_delay = int(os.getenv('TEST_DELAY', '60'))  # Base delay in seconds
        step_increment = int(os.getenv('TEST_STEP_INCREMENT', '30'))  # Increment between steps
        return {
            'base_delay': base_delay,
            'step_increment': step_increment
        }
    return None

async def update_sequence_status(sequence_id: str):
    """Update sequence status based on audit records"""
    try:
        # Get all audit records for this sequence
        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        
        if not audits:
            return
        
        # Check if all audits are completed or failed
        all_completed = all(audit["status"] in ["SENT", "FAILED", "CANCELLED"] for audit in audits)
        any_failed = any(audit["status"] in ["FAILED", "CANCELLED"] for audit in audits)
        
        new_status = "COMPLETED" if all_completed and not any_failed else \
                    "FAILED" if all_completed and any_failed else \
                    "IN_PROGRESS"

        # Update sequence status
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        logger.info(f"Updated sequence {sequence_id} status to {new_status}")

    except Exception as e:
        logger.error(f"Error updating sequence status: {str(e)}")

# Move cleanup task to a test utilities module
@celery_app.task(name='cleanup_test_duplicates', shared=True)
def cleanup_test_duplicates():
    """Clean up duplicate test mode entries - only runs in test mode."""
    if os.getenv('TEST_MODE') != 'true':
        logger.info("Cleanup task skipped - not in test mode")
        return 0
        
    try:
        # Find sequences with test mode duplicates
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "sequence_id": "$sequence_id",
                        "step_index": "$step_index"
                    },
                    "count": {"$sum": 1},
                    "docs": {"$push": "$$ROOT"}
                }
            },
            {
                "$match": {
                    "count": {"$gt": 1}
                }
            }
        ]

        duplicates = sequence_audit_collection.aggregate(pipeline)

        for duplicate in duplicates:
            docs = sorted(duplicate["docs"], key=lambda x: x["created_at"], reverse=True)
            kept_doc = docs[0]

            # Update other docs to cancelled
            for doc in docs[1:]:
                sequence_audit_collection.update_one(
                    {"_id": doc["_id"]},
                    {
                        "$set": {
                            "status": "CANCELLED",
                            "error_message": "Duplicate test mode entry",
                            "updated_at": datetime.utcnow()
                        }
                    }
                )

            # Update sequence status synchronously since we're in a Celery task
            if kept_doc.get("sequence_id"):
                update_sequence_status_sync(kept_doc["sequence_id"])

    except Exception as e:
        logger.error(f"Error cleaning up test duplicates: {str(e)}")

def update_sequence_status_sync(sequence_id: str):
    """Synchronous version of update_sequence_status for Celery tasks"""
    try:
        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        if not audits:
            return
        
        all_completed = all(audit["status"] in ["SENT", "FAILED", "CANCELLED"] for audit in audits)
        any_failed = any(audit["status"] in ["FAILED", "CANCELLED"] for audit in audits)
        
        new_status = "COMPLETED" if all_completed and not any_failed else \
                    "FAILED" if all_completed and any_failed else \
                    "IN_PROGRESS"

        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        logger.info(f"Updated sequence {sequence_id} status to {new_status}")
    except Exception as e:
        logger.error(f"Error updating sequence status: {str(e)}")

def check_for_replies_sync(service, thread_id: str, sender_email: str) -> bool:
    """Synchronous version of check_for_replies."""
    try:
        thread = service.users().threads().get(
            userId='me',
            id=thread_id,
            format='metadata',
            metadataHeaders=['From']
        ).execute()

        messages = thread.get('messages', [])
        if len(messages) <= 1:  # Only our message exists
            return False

        # Check if any message is from someone other than the sender
        for message in messages[1:]:  # Skip first message (our original email)
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            from_email = headers.get('From', '').lower()
            if sender_email.lower() not in from_email:
                logger.info(f"Reply detected from {from_email} in thread {thread_id}")
                return True

        return False

    except Exception as e:
        logger.error(f"Error checking replies: {str(e)}")
        return False

def cancel_remaining_steps_sync(sequence_id: str, reason: str = "Recipient replied to email"):
    """Synchronous version of cancel_remaining_steps."""
    try:
        # Find all scheduled audits for this sequence
        scheduled_audits = sequence_audit_collection.find({
            "sequence_id": sequence_id,
            "status": "SCHEDULED"
        })

        for audit in scheduled_audits:
            # Instead of terminating, just revoke the task
            if audit.get('schedule_id'):
                celery_app.control.revoke(
                    audit['schedule_id'], 
                    terminate=False  # Changed from True to False
                )
                logger.info(f"Revoked task {audit['schedule_id']}")

            # Update audit status
            sequence_audit_collection.update_one(
                {"_id": audit["_id"]},
                {"$set": {
                    "status": "CANCELLED",
                    "error_message": reason,
                    "updated_at": datetime.utcnow()
                }}
            )
            logger.info(f"Updated audit {audit['_id']} status to CANCELLED")

        # Update sequence status
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {"$set": {
                "status": "COMPLETED",
                "completion_reason": reason,
                "thread_id": None,  # Clear thread_id to prevent further sends
                "updated_at": datetime.utcnow()
            }}
        )
        logger.info(f"Updated sequence {sequence_id} status to COMPLETED")

    except Exception as e:
        logger.error(f"Error canceling remaining steps: {str(e)}")
        raise

@celery_app.task
def send_scheduled_email(email_payload: dict, scheduled_time: str = None, token_data: dict = None):
    """Celery task for sending scheduled emails."""
    try:
        logger.info(f"Processing email task with payload: {email_payload}")
        
        sequence_id = email_payload.get('sequence_id')
        audit_id = email_payload.get('audit_id')
        thread_id = email_payload.get('thread_id')  # Get thread_id from payload
        sequence = None  # Initialize sequence variable

        # Get sequence info for threading
        if sequence_id:
            sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
            if sequence:
                # Use thread info from sequence if available
                thread_id = thread_id or sequence.get('thread_id')
                email_payload['thread_id'] = thread_id
                
                # Use original subject for follow-ups
                if sequence.get('original_subject') and not email_payload.get('is_initial'):
                    email_payload['subject'] = sequence['original_subject']
                    logger.info(f"Using original subject: {email_payload['subject']}")

        # Check for replies before sending follow-up
        if sequence and thread_id and not email_payload.get('is_initial'):
            try:
                # Build Gmail service
                creds = Credentials(
                    token=token_data["accessToken"],
                    refresh_token=token_data["refreshToken"],
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=token_data["clientId"],
                    client_secret=token_data["clientSecret"],
                    scopes=token_data["scope"].split()
                )
                
                service = build('gmail', 'v1', credentials=creds)
                
                # Check for replies using sync version
                has_reply = check_for_replies_sync(
                    service, 
                    thread_id,
                    token_data.get("userEmail")
                )
                
                if has_reply:
                    logger.info(f"Reply detected in thread {thread_id}, canceling sequence {sequence_id}")
                    cancel_remaining_steps_sync(sequence_id)
                    return {
                        "status": "cancelled",
                        "message": "Sequence cancelled - recipient replied to email"
                    }
                    
            except Exception as e:
                logger.error(f"Error checking for replies: {str(e)}")
                # Continue with send if reply check fails

        # Add check for already cancelled sequence
        if sequence_id:
            sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
            if sequence and sequence.get("status") in ["COMPLETED", "CANCELLED"]:
                logger.info(f"Sequence {sequence_id} is already {sequence['status']}, skipping email")
                return {
                    "status": "cancelled",
                    "message": f"Sequence is {sequence['status']}"
                }

        # Send email
        from talentwizer_commons.utils.email import send_email_from_user_email, EmailPayload
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Convert to EmailPayload and ensure thread info is included
            email_obj = EmailPayload(**{
                k: v for k, v in email_payload.items() 
                if k in EmailPayload.__fields__
            })
            
            # Send email with thread_id
            result = loop.run_until_complete(
                send_email_from_user_email(
                    token_data,
                    email_obj,
                    thread_id=thread_id  # Pass thread_id to email function
                )
            )

            if result["status_code"] == 200:
                # For initial email, store thread info in sequence
                if email_payload.get('is_initial'):
                    sequence_collection.update_one(
                        {"_id": ObjectId(sequence_id)},
                        {
                            "$set": {
                                "thread_id": result['threadId'],
                                "original_subject": email_payload['subject'],
                                "status": "IN_PROGRESS",
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )

                # Update audit status
                sequence_audit_collection.update_one(
                    {"_id": ObjectId(audit_id)},
                    {
                        "$set": {
                            "status": "SENT",
                            "sent_time": datetime.utcnow(),
                            "thread_id": result.get('threadId') or thread_id,
                            "updated_at": datetime.utcnow()
                        }
                    }
                )

            # Update sequence status
            update_sequence_status_sync(sequence_id)
            
            return {"status": "sent", "result": result}

        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error in send_scheduled_email: {str(e)}", exc_info=True)
        if email_payload.get('audit_id'):
            sequence_audit_collection.update_one(
                {"_id": ObjectId(email_payload['audit_id'])},
                {
                    "$set": {
                        "status": "FAILED",
                        "error_message": str(e),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        raise

# Use a simpler singleton pattern
_task_restore_complete = False

@celery_app.task(bind=True, name='restore_persisted_tasks')
def restore_persisted_tasks(self):
    """Task to restore persisted tasks on worker startup."""
    global _task_restore_complete
    
    if _task_restore_complete:
        logger.info("Tasks already restored, skipping...")
        return 0

    try:
        from .task_restore import restore_tasks
        result = restore_tasks()
        _task_restore_complete = True
        return result
    except Exception as e:
        logger.error(f"Task restoration failed: {str(e)}")
        return 0

@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """Run task restoration exactly once when worker is ready."""
    global _task_restore_complete
    if not _task_restore_complete:
        restore_persisted_tasks.apply_async(countdown=5)

# Add logger setup
@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    """Configure logging for Celery."""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Add your logging configuration here if needed

# Add task event handlers
@task_sent.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    """Handle task sent event."""
    task_id = headers.get('id') if headers else None
    if task_id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{task_id}',
                json.dumps({
                    'status': PENDING,
                    'sent': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_sent_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

@task_received.connect
def task_received_handler(sender=None, request=None, **kwargs):
    """Handle task received event."""
    if request and request.id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{request.id}',
                json.dumps({
                    'status': PENDING,
                    'received': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_received_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """Handle task success event."""
    if sender and sender.request.id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps({
                    'status': SUCCESS,
                    'result': str(result),
                    'completed': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_success_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

@task_failure.connect
def task_failure_handler(sender=None, exception=None, **kwargs):
    """Handle task failure event."""
    if sender and sender.request.id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps({
                    'status': FAILURE,
                    'error': str(exception),
                    'failed': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_failure_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

if __name__ == '__main__':
    initialize()
    celery_app.start()