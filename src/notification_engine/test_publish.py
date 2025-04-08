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
        setup_logger("notification_engine", level=None)
        logger.info("Starting test publisher")

        # Initialize RabbitMQ
        rabbitmq = RabbitMQ(
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            port=int(os.getenv("RABBITMQ_PORT", "5672")),
        )

        # Initialize OneSignal config and worker
        onesignal_config = OneSignalConfig(
            app_id=os.getenv("ONESIGNAL_APP_ID", ""),
            rest_api_key=os.getenv("ONESIGNAL_REST_API_KEY", ""),
        )
        worker = NotificationWorker(onesignal_config)

        # Initialize queue service
        queue_service = QueueService(rabbitmq, worker)

        # Connect to RabbitMQ
        await rabbitmq.connect()
        await rabbitmq.setup_channel()

        # Test notification data
        test_message = {
            "contents": {"en": "Test notification message"},
            "headings": {"en": "Test Notification"},
            "included_segments": ["All"],
            "data": {"type": "TEST"},
        }

        # Publish test message
        await queue_service.publish_message(test_message)
        logger.info("Test message published")

        # Close connection
        await rabbitmq.close()

    except Exception as e:
        logger.error(f"Error in test publisher: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
