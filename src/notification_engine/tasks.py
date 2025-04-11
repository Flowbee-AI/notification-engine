import json
import backoff
from celery import shared_task

from .modules.onesignal.client import OneSignalClient
from .config.onesignal_config import OneSignalConfig
from .models.notification_model import NotificationObj
from .config.settings import settings
from .utils.logger import logger
from .utils.metrics import metrics


@shared_task(
    bind=True,
    name="notification_engine.tasks.send_notification",
    max_retries=settings.onesignal_max_retries,
    default_retry_delay=settings.onesignal_retry_delay,
    acks_late=True,
    queue=settings.rabbitmq_queue_name,
)
def send_notification(self, notification_data):
    """
    Send a notification through OneSignal

    Args:
        notification_data (dict): Notification data
    """
    try:
        # Create notification object from data
        notification_obj = NotificationObj(**notification_data)
        logger.info(f"Processing notification message: {notification_obj}")
        print(f"Processing notification message: {notification_obj}")
        # Initialize OneSignal client
        onesignal_config = OneSignalConfig(
            app_id=settings.onesignal_app_id,
            rest_api_key=settings.onesignal_rest_api_key,
            api_url=settings.onesignal_api_url,
        )
        onesignal_client = OneSignalClient(onesignal_config)

        # Send notification through OneSignal (synchronously in Celery task)
        result = onesignal_client.create_notification_sync(
            contents=notification_obj.contents,
            headings=notification_obj.headings,
            include_external_user_ids=notification_obj.external_ids,
            data=notification_obj.data,
        )

        metrics.increment("notifications_sent")
        logger.info(f"Notification sent successfully: {result}")

        return result

    except Exception as e:
        logger.error(f"Error processing notification message: {str(e)}")
        metrics.increment("messages_failed")
        raise self.retry(
            exc=e, countdown=self.default_retry_delay * (2**self.request.retries)
        )
