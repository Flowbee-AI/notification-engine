import json
import asyncio
from typing import Callable, Dict, Any, Optional
from functools import wraps
import backoff
from aio_pika import Message
from .rabbitmq import RabbitMQ
from ..onesignal.client import OneSignalClient
from ...config.onesignal_config import OneSignalConfig
from ...config.settings import settings
from ...utils.logger import logger
from ...utils.metrics import metrics


class NotificationWorker:
    def __init__(self, onesignal_client: OneSignalClient):
        self.onesignal_client = onesignal_client
        self._processing = False

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=settings.onesignal.max_retries,
        max_time=30,
    )
    async def process_message(self, message: Message) -> None:
        """
        Process a notification message from the queue
        """
        if self._processing:
            logger.warning("Worker is already processing a message")
            return

        self._processing = True
        start_time = asyncio.get_event_loop().time()

        try:
            # Decode and parse message
            body = message.body.decode()
            data = json.loads(body)
            logger.info(f"Processing notification message: {data}")

            # Extract notification details
            contents = data.get("contents", {})
            headings = data.get("headings")
            included_segments = data.get("included_segments")
            include_external_user_ids = data.get("include_external_user_ids")
            data = data.get("data")

            # Send notification through OneSignal
            result = await self.onesignal_client.create_notification(
                contents=contents,
                headings=headings,
                included_segments=included_segments,
                include_external_user_ids=include_external_user_ids,
                data=data,
            )

            # Record metrics
            processing_time = asyncio.get_event_loop().time() - start_time
            metrics.record_processing_time(processing_time)
            metrics.increment("notifications_sent")

            logger.info(f"Notification sent successfully: {result}")
            await message.ack()

        except json.JSONDecodeError as e:
            logger.error(f"Invalid message format: {str(e)}")
            await message.reject(requeue=False)
            metrics.increment("messages_rejected")

        except Exception as e:
            logger.error(f"Error processing notification message: {str(e)}")
            await message.reject(requeue=True)
            metrics.increment("messages_failed")
            raise

        finally:
            self._processing = False

    async def health_check(self) -> bool:
        """
        Perform a health check of the worker
        """
        try:
            # Check if we can create a test notification
            await self.onesignal_client.create_notification(
                contents={"en": "Health check"},
                included_segments=["All"],
            )
            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False

