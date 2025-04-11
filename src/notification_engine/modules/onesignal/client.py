import aiohttp
from typing import Dict, Any, Optional
from ...config.onesignal_config import OneSignalConfig


class OneSignalClient:
    def __init__(self, config: OneSignalConfig):
        self.config = config
        self.base_url = "https://onesignal.com/api/v1"
        self.headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Basic {self.config.rest_api_key}",
        }

    async def create_notification(
        self,
        contents: Dict[str, str],
        headings: Optional[Dict[str, str]] = None,
        include_external_user_ids: Optional[list] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create and send a notification through OneSignal
        """
        url = f"{self.base_url}/notifications"
        payload = {"app_id": self.config.app_id, "contents": contents}

        if headings:
            payload["headings"] = headings

        if not include_external_user_ids:
            payload["included_segments"] = ["All"]
        else:
            payload["include_aliases"] = {"external_id": include_external_user_ids}
            payload["target_channel"] = "push"

        if data:
            payload["data"] = data

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                return await response.json()

    async def cancel_notification(self, notification_id: str) -> Dict[str, Any]:
        """
        Cancel a scheduled or currently outgoing notification
        """
        url = f"{self.base_url}/notifications/{notification_id}"

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self.headers) as response:
                return await response.json()

    async def view_notification(self, notification_id: str) -> Dict[str, Any]:
        """
        View the details of a notification
        """
        url = f"{self.base_url}/notifications/{notification_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()
