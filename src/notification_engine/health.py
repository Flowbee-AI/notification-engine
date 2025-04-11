from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from notification_engine.config.onesignal_config import OneSignalConfig
from .modules.queue.worker import NotificationWorker
from .utils.metrics import metrics
from .config.settings import settings
from .modules.onesignal.client import OneSignalClient

app = FastAPI(title="Notification Engine Health Check")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a dependency to get the worker instance
def get_worker() -> NotificationWorker:
    return NotificationWorker(
        onesignal_client=OneSignalClient(
            config=OneSignalConfig(
                app_id=settings.onesignal_app_id,
                rest_api_key=settings.onesignal_rest_api_key,
                api_url=settings.onesignal_api_url,
            )
        )
    )


@app.get("/health")
async def health_check(
    worker: NotificationWorker = Depends(get_worker),
) -> Dict[str, Any]:
    """
    Health check endpoint that checks:
    1. Service uptime
    2. Worker health
    3. Basic metrics
    """
    try:
        # Check worker health
        worker_healthy = await worker.health_check()
        if not worker_healthy:
            raise HTTPException(status_code=503, detail="Worker is unhealthy")

        # Get metrics
        processing_stats = metrics.get_metric_stats("processing_time")
        uptime = metrics.get_uptime()

        return {
            "status": "healthy",
            "uptime_seconds": uptime,
            "metrics": {
                "messages_processed": metrics.get_counter("messages_processed"),
                "messages_failed": metrics.get_counter("messages_failed"),
                "messages_rejected": metrics.get_counter("messages_rejected"),
                "notifications_sent": metrics.get_counter("notifications_sent"),
                "processing_time": processing_stats,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Get detailed metrics about the service
    """
    return {
        "uptime_seconds": metrics.get_uptime(),
        "counters": {
            name: metrics.get_counter(name)
            for name in [
                "messages_processed",
                "messages_failed",
                "messages_rejected",
                "notifications_sent",
            ]
        },
        "processing_time": metrics.get_metric_stats("processing_time"),
    }


def start_health_server(worker: NotificationWorker) -> None:
    """
    Start the health check server
    """
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.health_check_port,
        log_level="info",
        reload=True,
    )
