import os
from dotenv import load_dotenv
from .celery_app import celery_app
from .tasks import send_notification
from .utils.logger import logger, setup_logger
from .config.settings import settings

# Load environment variables
load_dotenv()


def main():
    """
    Main entry point for the worker
    """
    try:
        # Set up logging
        setup_logger("notification_engine_worker", level=settings.log_level)
        logger.info("Starting Notification Engine Worker")

        # Start Celery worker - this will be called by the celery CLI
        # celery -A notification_engine.worker worker --loglevel=info
        pass

    except Exception as e:
        logger.error(f"Error in worker main: {str(e)}")
        raise


if __name__ == "__main__":
    main()
