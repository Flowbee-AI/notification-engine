import asyncio
import aio_pika
from ..config.settings import settings
from ..utils.logger import logger


async def delete_queue():
    try:
        # Connect to RabbitMQ
        connection = await aio_pika.connect_robust(
            host=settings.rabbitmq.host,
            port=settings.rabbitmq.port,
            login=settings.rabbitmq.username,
            password=settings.rabbitmq.password,
            virtualhost=settings.rabbitmq.vhost,
        )

        async with connection:
            # Create a channel
            channel = await connection.channel()

            # Delete the queue
            await channel.queue_delete(settings.rabbitmq.queue_name)
            logger.info(f"Successfully deleted queue: {settings.rabbitmq.queue_name}")

            # Delete the dead letter queue as well
            await channel.queue_delete("notification_dlq")
            logger.info("Successfully deleted dead letter queue: notification_dlq")

    except Exception as e:
        logger.error(f"Error deleting queue: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(delete_queue())
