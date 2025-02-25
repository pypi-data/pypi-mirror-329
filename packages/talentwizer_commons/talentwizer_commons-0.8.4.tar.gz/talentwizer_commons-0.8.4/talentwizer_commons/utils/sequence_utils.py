import logging
from datetime import datetime
from bson import ObjectId
from typing import Optional

logger = logging.getLogger(__name__)

def cancel_sequence_steps(mongo_db, sequence_id: str, celery_app, reason: str = "Recipient replied to email") -> None:
    """Cancel remaining steps in a sequence."""
    try:
        sequence_audit_collection = mongo_db["email_sequence_audits"]
        sequence_collection = mongo_db["email_sequences"]
        
        # Find all scheduled audits for this sequence
        scheduled_audits = sequence_audit_collection.find({
            "sequence_id": sequence_id,
            "status": "SCHEDULED"
        })

        for audit in scheduled_audits:
            if audit.get("schedule_id"):
                # Revoke the Celery task
                celery_app.control.revoke(audit["schedule_id"], terminate=False)
                
            # Update audit status
            sequence_audit_collection.update_one(
                {"_id": audit["_id"]},
                {
                    "$set": {
                        "status": "CANCELLED",
                        "updated_at": datetime.utcnow(),
                        "cancel_reason": reason
                    }
                }
            )
        
        # Update sequence status
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": "COMPLETED",
                    "updated_at": datetime.utcnow(),
                    "completion_reason": reason
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error cancelling sequence steps: {str(e)}")
        raise

def update_sequence_status(mongo_db, sequence_id: str, step_count: Optional[int] = None) -> None:
    """Update sequence status based on completed steps."""
    try:
        sequence_audit_collection = mongo_db["email_sequence_audits"]
        sequence_collection = mongo_db["email_sequences"]
        
        # Get all audits for this sequence
        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        
        if not audits:
            return
        
        total_steps = step_count if step_count is not None else len(audits)
        completed_steps = sum(1 for audit in audits if audit["status"] in ["SENT", "CANCELLED"])
        
        # Calculate new status
        if completed_steps == 0:
            new_status = "PENDING"
        elif completed_steps < total_steps:
            new_status = "IN_PROGRESS"
        else:
            new_status = "COMPLETED"
            
        # Update sequence
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.utcnow(),
                    "progress": {
                        "completed": completed_steps,
                        "total": total_steps
                    }
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error updating sequence status: {str(e)}")
        raise
