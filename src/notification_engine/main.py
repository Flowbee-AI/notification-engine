import asyncio
import signal
from typing import List

from dotenv import load_dotenv
from notification_engine.config.settings import settings
from notification_engine.config.onesignal_config import OneSignalConfig
from notification_engine.modules.queue.rabbitmq import RabbitMQ
from notification_engine.modules.queue.worker import NotificationWorker
from notification_engine.modules.queue.queue_service import QueueService
from notification_engine.modules.onesignal.client import OneSignalClient
from notification_engine.utils.logger import logger, setup_logger
from notification_engine.utils.metrics import metrics
from notification_engine.health import start_health_server

# Load environment variables
load_dotenv(dotenv_path=".env")


async def shutdown(signal, loop, queue_service):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {signal.name}...")

    logger.info("Stopping queue service...")
    await queue_service.stop()

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]

    logger.info(f"Cancelling {len(tasks)} outstanding tasks...")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    logger.info("Shutdown complete.")


async def main():
    try:
        # Set up logging
        setup_logger("notification_engine", level=settings.log_level)
        logger.info("Starting Notification Engine")

        # Initialize OneSignal client
        onesignal_config = OneSignalConfig(
            app_id=settings.onesignal_app_id,
            rest_api_key=settings.onesignal_rest_api_key,
            api_url=settings.onesignal_api_url,
        )
        onesignal_client = OneSignalClient(onesignal_config)

        # Initialize RabbitMQ
        rabbitmq = await RabbitMQ.get_instance()

        # Initialize worker and queue service
        worker = NotificationWorker(onesignal_client)
        queue_service = QueueService(rabbitmq, worker)

        # Start the queue service
        await queue_service.start()

        # Start health check server in a separate process
        import multiprocessing

        health_server = multiprocessing.Process(
            target=start_health_server, args=(worker,)
        )
        health_server.start()

        # Set up signal handlers for graceful shutdown
        loop = asyncio.get_running_loop()
        signals = (signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(
                s, lambda s=s: asyncio.create_task(shutdown(s, loop, queue_service))
            )

        # Keep the service running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour, or until interrupted

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise
