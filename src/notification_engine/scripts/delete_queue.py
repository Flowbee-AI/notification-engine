import asyncio
import aio_pika
from notification_engine.config.settings import settings
from notification_engine.utils.logger import logger


async def delete_queue():
    try:
        # Connect to RabbitMQ
        connection_params = {
            "host": settings.rabbitmq_host,
            "port": settings.rabbitmq_port,
            "login": settings.rabbitmq_username,
            "password": settings.rabbitmq_password,
            "virtualhost": settings.rabbitmq_vhost,
        }
        
        # Add SSL if enabled
        if settings.rabbitmq_ssl:
            connection_params["ssl"] = True
            
        connection = await aio_pika.connect_robust(**connection_params)

        async with connection:
            # Create a channel
            channel = await connection.channel()

            # Delete the queue
            await channel.queue_delete(settings.rabbitmq_queue_name)
            logger.info(f"Successfully deleted queue: {settings.rabbitmq_queue_name}")

            # Delete the dead letter queue as well
            await channel.queue_delete("notification_dlq")
            logger.info("Successfully deleted dead letter queue: notification_dlq")

    except Exception as e:
        logger.error(f"Error deleting queue: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(delete_queue())
