import os
from typing import Dict, Any
import requests
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class OneSignalConfig:
    """
    Configuration class for OneSignal
    """

    app_id: str
    rest_api_key: str
    api_url: str
