import requests
import json
import os
import sys
import time
from dotenv import load_dotenv

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Load environment variables
load_dotenv()


def test_send_notification():
    """
    Test sending a notification using the API
    """
    # API endpoint
    url = "http://localhost:8000/api/notifications/send"

    # Test notification data
    notification_data = {
        "contents": {"en": "Test notification from Celery"},
        "headings": {"en": "Celery Test Notification"},
        "data": {"type": "TEST"},
        "external_ids": ["test_user_id"],
    }

    # Send request
    print(f"Sending notification to {url}")
    response = requests.post(url, json=notification_data)

    if response.status_code == 200:
        result = response.json()
        print(f"Notification queued successfully!")
        print(f"Task ID: {result['task_id']}")
        print(f"Status: {result['status']}")

        # Check status after a delay
        time.sleep(2)
        status_url = (
            f"http://localhost:8000/api/notifications/status/{result['task_id']}"
        )
        status_response = requests.get(status_url)
        if status_response.status_code == 200:
            status_result = status_response.json()
            print(f"Task status: {status_result['status']}")
            if "result" in status_result and status_result["result"]:
                print(f"Task result: {json.dumps(status_result['result'], indent=2)}")
    else:
        print(f"Error sending notification: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    test_send_notification()
