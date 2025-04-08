from typing import Dict, Any, Callable
import json
from .rabbitmq import RabbitMQ
from .worker import NotificationWorker
from ...utils.logger import logger


class QueueService:
    def __init__(self, rabbitmq: RabbitMQ, worker: NotificationWorker):
        self.rabbitmq = rabbitmq
        self.worker = worker

    async def start(self) -> None:
        """
        Start the queue service
        """
        logger.info("Starting queue service")
        await self.rabbitmq.initialize()
        await self.rabbitmq.setup_channel()
        await self.consume_messages()

    async def stop(self) -> None:
        """
        Stop the queue service
        """
        logger.info("Stopping queue service")
        await self.rabbitmq.close()

    async def consume_messages(self) -> None:
        """
        Consume messages from the queue
        """

        async def message_handler(message: Dict[str, Any]) -> None:
            try:
                await self.worker.process_message(message)
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")

        logger.info("Starting to consume messages")
        await self.rabbitmq.consume(message_handler)

    async def publish_message(self, message: Dict[str, Any]) -> None:
        """
        Publish a message to the queue
        """
        try:
            logger.info("Publishing message to queue")
            await self.rabbitmq.publish(message)
            logger.info("Message published successfully")
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            raise
