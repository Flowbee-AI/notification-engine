from celery import Celery
from notification_engine.config.settings import settings
import os

# Initialize Celery with RabbitMQ broker using SSL
broker_url = f"amqps://{settings.rabbitmq_username}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/{settings.rabbitmq_vhost}"

# Create a results directory if it doesn't exist
results_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results"
)
os.makedirs(results_dir, exist_ok=True)

celery_app = Celery(
    "notification_engine",
    broker=broker_url,
    # Use a simple file-based backend
    backend=f"file://{results_dir}",
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "notification_engine.tasks.*": {"queue": settings.rabbitmq_queue_name},
    },
    broker_transport_options={
        "confirm_publish": True,
        "ssl": True,
    },
)
celery_app.autodiscover_tasks(["notification_engine.tasks"])
# test connection
print(celery_app.control.ping())
