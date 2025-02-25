from datetime import datetime, timedelta
import redis
from bson import ObjectId
import logging
from .db import mongo_database, get_redis_client  # Import get_redis_client from db
from .celery_init import celery_app, get_redis_url
from celery.app.control import Inspect

logger = logging.getLogger(__name__)

def cleanup_completed_tasks():
    """Clean up completed tasks from Redis that are marked as complete in MongoDB"""
    try:
        redis_client = get_redis_client()
        sequence_audit_collection = mongo_database["email_sequence_audits"]

        # Get all tasks from Redis unacked queue
        unacked_tasks = redis_client.zrange('celery:unacked', 0, -1)
        
        for task_id in unacked_tasks:
            task_id = task_id.decode() if isinstance(task_id, bytes) else task_id
            
            # Check if task is completed in MongoDB
            audit = sequence_audit_collection.find_one({
                "schedule_id": task_id,
                "status": {"$in": ["SENT", "FAILED", "CANCELLED"]}
            })
            
            if audit:
                # Task is completed, remove from Redis
                redis_client.zrem('celery:unacked', task_id)
                logger.info(f"Cleaned up completed task {task_id} from Redis")

    except Exception as e:
        logger.error(f"Error cleaning up completed tasks: {e}")
        return False

def get_consolidated_task_status(hours_back: int = 24, include_completed: bool = False):
    """Get consolidated view of tasks from Redis, Celery, and MongoDB."""
    try:
        stats = {
            "total_tasks": 0,
            "active_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "scheduled_tasks": 0,
            "tasks": [],
            "redis_status": "unknown",
            "celery_status": "unknown",
            "db_status": "unknown",
            "last_updated": datetime.utcnow().isoformat()
        }

        # MongoDB stats
        sequence_audit_collection = mongo_database["email_sequence_audits"]
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        pipeline = [
            {
                "$match": {
                    "created_at": {"$gte": cutoff_time},
                    # Only include non-completed tasks when requested
                    "status": {"$nin": ["SENT", "FAILED", "CANCELLED"]} if not include_completed else {"$exists": True}
                }
            },
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "tasks": {
                        "$push": {
                            "task_id": "$schedule_id",
                            "sequence_id": "$sequence_id",
                            "status": "$status",
                            "scheduled_time": "$scheduled_time",
                            "sent_time": "$sent_time",
                            "error": "$error_message",
                            "created_at": "$created_at",
                            "email": {"$arrayElemAt": ["$email_payload.to_email", 0]},
                            "subject": "$email_payload.subject"
                        }
                    }
                }
            }
        ]

        db_results = list(sequence_audit_collection.aggregate(pipeline))
        stats["db_status"] = "connected"

        # Run cleanup synchronously
        cleanup_completed_tasks()

        # Redis stats
        try:
            redis_client = get_redis_client()  # Use the centralized Redis client
            redis_client.ping()  # Test connection
            stats["redis_status"] = "connected"
            
            # Get counts from different Redis queues
            for queue in ['unacked', 'reserved', 'scheduled']:
                queue_key = f"celery:{queue}"
                try:
                    count = redis_client.zcard(queue_key)
                    stats[f"redis_{queue}"] = count
                    if queue == 'scheduled':
                        stats["scheduled_tasks"] += count
                except Exception as queue_error:
                    logger.warning(f"Error getting count for queue {queue_key}: {str(queue_error)}")
                    stats[f"redis_{queue}"] = 0

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {str(e)}")
            stats["redis_status"] = f"error: {str(e)}"
        except Exception as e:
            logger.error(f"Redis error: {str(e)}")
            stats["redis_status"] = f"error: {str(e)}"

        # Celery stats
        try:
            i = celery_app.control.inspect(timeout=2.0)  # Use celery_app.control directly
            active = i.active() or {}
            scheduled = i.scheduled() or {}
            reserved = i.reserved() or {}
            
            stats["celery_status"] = "connected"
            stats["active_tasks"] = sum(len(tasks) for tasks in active.values())
            stats["scheduled_tasks"] += sum(len(tasks) for tasks in scheduled.values())
            stats["reserved_tasks"] = sum(len(tasks) for tasks in reserved.values())

        except ConnectionError as e:
            logger.error(f"Celery connection error: {str(e)}")
            stats["celery_status"] = f"error: {str(e)}"
        except Exception as e:
            logger.error(f"Celery error: {str(e)}")
            stats["celery_status"] = f"error: {str(e)}"

        # Aggregate task data
        for result in db_results:
            status = result["_id"]
            count = result["count"]
            
            if status == "SENT":
                stats["completed_tasks"] += count
            elif status == "FAILED":
                stats["failed_tasks"] += count
            
            stats["total_tasks"] += count
            stats["tasks"].extend(result["tasks"])

        # Sort tasks by scheduled_time
        stats["tasks"].sort(key=lambda x: x.get("scheduled_time", datetime.max), reverse=True)

        return stats

    except Exception as e:
        logger.error(f"Error getting consolidated task status: {str(e)}")
        raise
