import asyncio
from dotenv import load_dotenv
from notification_engine.config.settings import settings
from notification_engine.config.onesignal_config import OneSignalConfig
from notification_engine.modules.queue.rabbitmq import RabbitMQ
from notification_engine.modules.queue.worker import NotificationWorker
from notification_engine.modules.queue.queue_service import QueueService
from notification_engine.modules.onesignal.client import OneSignalClient
from notification_engine.utils.logger import logger, setup_logger

# Load environment variables
load_dotenv()


async def main():
    try:
        # Set up logging
        setup_logger("notification_engine", level=settings.log_level)
        logger.info("Starting test publisher")

        # Initialize OneSignal client
        onesignal_config = OneSignalConfig(
            app_id=settings.onesignal.app_id,
            rest_api_key=settings.onesignal.rest_api_key,
            api_url=settings.onesignal.api_url,
        )
        onesignal_client = OneSignalClient(onesignal_config)

        # Initialize RabbitMQ
        rabbitmq = await RabbitMQ.get_instance()

        # Initialize worker and queue service
        worker = NotificationWorker(onesignal_client)
        queue_service = QueueService(rabbitmq, worker)

        # Initialize RabbitMQ connection
        await rabbitmq.initialize()
        await rabbitmq.setup_channel()

        # Test notification data
        test_message = {
            "contents": {"en": "Test notification message"},
            "headings": {"en": "Test Notification"},
            "included_segments": ["All"],
            "data": {"type": "TEST"},
            "external_id": "LvDnIj8Qu9gWd0qEib2RGaHS2hg1",
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
