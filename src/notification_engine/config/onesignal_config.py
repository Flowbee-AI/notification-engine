from dotenv import load_dotenv
from dataclasses import dataclass
from notification_engine.config.settings import settings


@dataclass
class OneSignalConfig:
    """
    Configuration class for OneSignal
    """

    app_id: str = settings.onesignal_app_id
    rest_api_key: str = settings.onesignal_rest_api_key
    api_url: str = settings.onesignal_api_url
