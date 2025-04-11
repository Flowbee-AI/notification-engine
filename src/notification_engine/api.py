from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from notification_engine.models.notification_model import NotificationObj
from notification_engine.celery_app import celery_app
from notification_engine.tasks import send_notification
from notification_engine.utils.logger import logger, setup_logger
from notification_engine.config.settings import settings

# Set up logging
setup_logger("notification_engine_api", level=settings.log_level)

# Create FastAPI app
app = FastAPI(
    title="Notification Engine API",
    description="API for sending notifications via Celery and OneSignal",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class NotificationResponse(BaseModel):
    task_id: str
    status: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None


@app.post("/api/notifications/send", response_model=NotificationResponse)
async def send_notification_endpoint(notification: NotificationObj):
    """
    Send a notification via Celery task
    """
    try:
        # Submit task to Celery
        print(f"Sending notification: {notification.model_dump()}")
        # Log broker URL for debugging
        broker_url = celery_app.conf.broker_url
        logger.info(f"Using broker URL: {broker_url}")
        task = send_notification.delay(notification.model_dump())
        print(f"Task submitted: {task.id}")
        logger.info(f"Notification task submitted: {task.id}")
        return {"task_id": task.id, "status": "queued"}
    except ConnectionRefusedError as e:
        error_msg = f"Connection refused to message broker: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        logger.error(f"Error submitting notification task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/notifications/status/{task_id}", response_model=TaskStatusResponse)
async def get_notification_status(task_id: str):
    """
    Get the status of a notification task
    """
    try:
        task = send_notification.AsyncResult(task_id)
        response = {
            "task_id": task_id,
            "status": task.status,
        }

        if task.ready():
            response["result"] = task.result

        return response
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    health_data = {"status": "healthy", "components": {}}

    # Check Celery/RabbitMQ connection
    try:
        ping_result = celery_app.control.ping(timeout=1.0)
        health_data["components"]["celery"] = {
            "status": "up" if ping_result else "down",
            "details": ping_result or "No response from Celery workers",
        }
    except Exception as e:
        health_data["components"]["celery"] = {"status": "down", "error": str(e)}
        health_data["status"] = "degraded"

    return health_data
