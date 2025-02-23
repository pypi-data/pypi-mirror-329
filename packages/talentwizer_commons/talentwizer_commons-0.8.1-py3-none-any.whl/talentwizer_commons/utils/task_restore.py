import os
import redis
import logging
from datetime import datetime
import json
from .celery_init import celery_app, send_scheduled_email
from .db import mongo_database

logger = logging.getLogger(__name__)

def restore_tasks():
    """Restore and reschedule tasks from MongoDB."""
    try:
        logger.info("Starting task restoration process...")
        restored_count = 0
        sequence_audit_collection = mongo_database["email_sequence_audits"]

        # Find all SCHEDULED tasks that were not sent
        pending_tasks = sequence_audit_collection.find({
            "status": "SCHEDULED",
            "scheduled_time": {"$lt": datetime.utcnow()}  # Only get overdue tasks
        })

        for task in pending_tasks:
            try:
                # Create new task for immediate execution
                new_task = send_scheduled_email.apply_async(
                    kwargs={
                        'email_payload': task['email_payload'],
                        'token_data': task.get('token_data'),
                        'scheduled_time': datetime.utcnow().isoformat()
                    },
                    queue='email_queue',
                    routing_key='email.send'
                )

                # Update audit record with new task ID
                sequence_audit_collection.update_one(
                    {"_id": task["_id"]},
                    {
                        "$set": {
                            "schedule_id": new_task.id,
                            "rescheduled_from": task.get("schedule_id"),
                            "rescheduled_at": datetime.utcnow()
                        }
                    }
                )

                logger.info(f"Restored task {task.get('schedule_id')} with new task ID {new_task.id}")
                restored_count += 1

            except Exception as task_error:
                logger.error(f"Failed to restore task {task.get('schedule_id')}: {str(task_error)}")
                continue

        logger.info(f"Task restoration completed. Restored {restored_count} tasks")
        return restored_count

    except Exception as e:
        logger.error(f"Task restoration failed: {str(e)}")
        return 0
