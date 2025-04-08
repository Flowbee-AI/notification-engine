import asyncio
import os
from dotenv import load_dotenv
from .config.onesignal_config import OneSignalConfig
from .modules.queue.rabbitmq import RabbitMQ
from .modules.queue.worker import NotificationWorker
from .modules.queue.queue_service import QueueService
from .utils.logger import logger, setup_logger

# Load environment variables
load_dotenv()


async def main():
    try:
        # Set up logging
        setup_logger("notification_engine", level=None)  # Uses INFO level by default
        logger.info("Starting Notification Engine")

        # Initialize OneSignal configuration
        onesignal_config = OneSignalConfig(
            app_id=os.getenv("ONESIGNAL_APP_ID", ""),
            rest_api_key=os.getenv("ONESIGNAL_REST_API_KEY", ""),
        )

        # Initialize RabbitMQ
        rabbitmq = RabbitMQ(
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            port=int(os.getenv("RABBITMQ_PORT", "5672")),
        )

        # Initialize worker and queue service
        worker = NotificationWorker(onesignal_config)
        queue_service = QueueService(rabbitmq, worker)

        # Start the queue service
        await queue_service.start()

        # Keep the service running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        finally:
            await queue_service.stop()

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
