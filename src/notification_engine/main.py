import uvicorn
import os
from dotenv import load_dotenv
from notification_engine.api import app
from notification_engine.utils.logger import logger, setup_logger
from notification_engine.config.settings import settings

# Load environment variables
load_dotenv()


def main():
    """
    Main entry point for the API server
    """
    try:
        # Set up logging
        setup_logger("notification_engine", level=settings.log_level)
        logger.info("Starting Notification Engine API")

        # Run the FastAPI app
        uvicorn.run(
            "notification_engine.api:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", "8000")),
            reload=True,
            log_level=settings.log_level.lower(),
        )
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise


if __name__ == "__main__":
    main()
