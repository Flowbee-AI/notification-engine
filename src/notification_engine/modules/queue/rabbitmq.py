import json
import aio_pika
from typing import Dict, Any, Callable, Optional
from ...utils.logger import logger


class RabbitMQ:
    def __init__(self, host: str = "localhost", port: int = 5672):
        self.host = host
        self.port = port
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue_name = "notifications"

    async def connect(self) -> None:
        """
        Connect to RabbitMQ server
        """
        try:
            logger.info(f"Connecting to RabbitMQ at {self.host}:{self.port}")
            self.connection = await aio_pika.connect_robust(
                f"amqp://guest:guest@{self.host}:{self.port}/"
            )
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise

    async def setup_channel(self) -> None:
        """
        Set up RabbitMQ channel and declare queue
        """
        if not self.connection:
            raise RuntimeError("Not connected to RabbitMQ")

        try:
            logger.info("Setting up RabbitMQ channel")
            self.channel = await self.connection.channel()
            await self.channel.declare_queue(self.queue_name, durable=True)
        except Exception as e:
            logger.error(f"Failed to setup RabbitMQ channel: {str(e)}")
            raise

    async def publish(self, message: Dict[str, Any]) -> None:
        """
        Publish a message to the queue
        """
        if not self.channel:
            raise RuntimeError("Channel not set up")

        try:
            logger.info(f"Publishing message to queue {self.queue_name}")
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=self.queue_name,
            )
            logger.info("Message published successfully")
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
            raise

    async def consume(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Consume messages from the queue
        """
        if not self.channel:
            raise RuntimeError("Channel not set up")

        try:
            queue = await self.channel.declare_queue(self.queue_name, durable=True)

            async def process_message(message: aio_pika.IncomingMessage) -> None:
                async with message.process():
                    try:
                        body = message.body.decode()
                        data = json.loads(body)
                        await callback(data)
                    except Exception as e:
                        logger.error(f"Error processing message: {str(e)}")
                        # Nack the message to requeue it
                        await message.nack(requeue=True)

            logger.info(f"Starting to consume messages from queue {self.queue_name}")
            await queue.consume(process_message)

        except Exception as e:
            logger.error(f"Failed to consume messages: {str(e)}")
            raise

    async def close(self) -> None:
        """
        Close the RabbitMQ connection
        """
        try:
            if self.channel:
                logger.info("Closing RabbitMQ channel")
                await self.channel.close()
            if self.connection:
                logger.info("Closing RabbitMQ connection")
                await self.connection.close()
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {str(e)}")
            raise
