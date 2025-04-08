import json
import aio_pika
from aio_pika import Connection, Channel, Exchange, Queue
from aio_pika.pool import Pool
from typing import Dict, Any, Callable, Optional
import asyncio
from functools import wraps
import backoff
from ...config.settings import settings
from ...utils.logger import logger
from ...utils.metrics import metrics


class RabbitMQ:
    _instance = None
    _connection_pool: Optional[Pool] = None
    _channel_pool: Optional[Pool] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitMQ, cls).__new__(cls)
        return cls._instance

    @classmethod
    async def get_instance(cls) -> "RabbitMQ":
        if cls._instance is None:
            cls._instance = RabbitMQ()
            await cls._instance.initialize()
        return cls._instance

    async def initialize(self) -> None:
        """Initialize connection and channel pools"""
        self._connection_pool = Pool(self._get_connection, max_size=10)
        self._channel_pool = Pool(self._get_channel, max_size=20)

    async def _get_connection(self) -> Connection:
        """Create a new connection"""
        return await aio_pika.connect_robust(
            host=settings.rabbitmq.host,
            port=settings.rabbitmq.port,
            login=settings.rabbitmq.username,
            password=settings.rabbitmq.password,
            virtualhost=settings.rabbitmq.vhost,
        )

    async def _get_channel(self) -> Channel:
        """Create a new channel"""
        async with self._connection_pool.acquire() as connection:
            return await connection.channel()

    @backoff.on_exception(
        backoff.expo,
        (aio_pika.exceptions.AMQPConnectionError, aio_pika.exceptions.AMQPChannelError),
        max_tries=settings.rabbitmq.retry_count,
        max_time=30,
    )
    async def setup_channel(self) -> None:
        """Set up the channel with exchange and queue"""
        async with self._channel_pool.acquire() as channel:
            # Declare exchange
            exchange = await channel.declare_exchange(
                "notification_exchange",
                aio_pika.ExchangeType.DIRECT,
                durable=True,
            )

            # Declare queue
            queue = await channel.declare_queue(
                settings.rabbitmq.queue_name,
                durable=True,
                arguments={
                    "x-dead-letter-exchange": "notification_dlx",
                    "x-dead-letter-routing-key": "notification_dlq",
                },
            )

            # Declare dead letter exchange and queue
            dlx = await channel.declare_exchange(
                "notification_dlx",
                aio_pika.ExchangeType.DIRECT,
                durable=True,
            )
            dlq = await channel.declare_queue(
                "notification_dlq",
                durable=True,
            )

            # Bind queues
            await queue.bind(exchange, "notification")
            await dlq.bind(dlx, "notification_dlq")

            # Set QoS
            await channel.set_qos(prefetch_count=settings.rabbitmq.prefetch_count)

    @backoff.on_exception(
        backoff.expo,
        (aio_pika.exceptions.AMQPConnectionError, aio_pika.exceptions.AMQPChannelError),
        max_tries=settings.rabbitmq.retry_count,
        max_time=30,
    )
    async def publish(self, message: Dict[str, Any]) -> None:
        """Publish a message to the queue"""
        async with self._channel_pool.acquire() as channel:
            exchange = await channel.get_exchange("notification_exchange")
            await exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key="notification",
            )
            metrics.increment("messages_published")

    @backoff.on_exception(
        backoff.expo,
        (aio_pika.exceptions.AMQPConnectionError, aio_pika.exceptions.AMQPChannelError),
        max_tries=settings.rabbitmq.retry_count,
        max_time=30,
    )
    async def consume(self, callback: callable) -> None:
        """Consume messages from the queue"""
        async with self._channel_pool.acquire() as channel:
            queue = await channel.get_queue(settings.rabbitmq.queue_name)
            await queue.consume(callback)

    async def close(self) -> None:
        """Close all connections"""
        if self._channel_pool:
            await self._channel_pool.close()
        if self._connection_pool:
            await self._connection_pool.close()
