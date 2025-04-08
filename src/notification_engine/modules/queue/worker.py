import json
import asyncio
from typing import Dict, Any, Callable
from .rabbitmq import RabbitMQ
from ..onesignal.client import OneSignalClient
from ...config.onesignal_config import OneSignalConfig
from ...utils.logger import logger


class NotificationWorker:
    def __init__(self, onesignal_config: OneSignalConfig):
        self.onesignal_client = OneSignalClient(onesignal_config)

    async def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process a notification message from the queue
        """
        try:
            logger.info(f"Processing notification message: {message}")

            # Extract notification details from message
            contents = message.get("contents", {})
            headings = message.get("headings")
            included_segments = message.get("included_segments")
            include_external_user_ids = message.get("include_external_user_ids")
            data = message.get("data")

            # Send notification through OneSignal
            result = await self.onesignal_client.create_notification(
                contents=contents,
                headings=headings,
                included_segments=included_segments,
                include_external_user_ids=include_external_user_ids,
                data=data,
            )

            logger.info(f"Notification sent successfully: {result}")

        except Exception as e:
            logger.error(f"Error processing notification message: {str(e)}")
            raise


class Worker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Worker, cls).__new__(cls)
        return cls._instance

    @classmethod
    async def get_instance(cls) -> "Worker":
        if cls._instance is None:
            cls._instance = Worker()
        return cls._instance

    async def start(self, job_function: Callable[[Dict[str, Any]], None]):
        rabbitmq = await RabbitMQ.get_instance()
        channel = rabbitmq.get_channel()

        def callback(ch, method, properties, body):
            try:
                data = json.loads(body)
                # Create and run the event loop for the coroutine
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(job_function(data))
                loop.close()
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="notification", on_message_callback=callback)
        channel.start_consuming()
