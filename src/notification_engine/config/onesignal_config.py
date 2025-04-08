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


class OneSignalClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OneSignalClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.app_id = os.getenv("ONESIGNAL_APP_ID")
        self.api_key = os.getenv("ONESIGNAL_API_KEY")
        self.base_url = "https://onesignal.com/api/v1/notifications"

    def send_notification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "app_id": self.app_id,
            "include_external_user_ids": [data["userId"]],
            "contents": {"en": data["payload"]["description"]},
            "headings": {"en": data["payload"]["title"]},
            "big_picture": data["payload"]["imageUrl"],
            "url": data["payload"]["link"],
            "data": {"type": data["payload"]["type"]},
        }

        response = requests.post(self.base_url, json=payload, headers=headers)
        return response.json()


# Create a singleton instance
one_signal_client = OneSignalClient()
