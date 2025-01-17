from datetime import datetime

import requests
from infinitystones.timestone.config.settings import Settings
from infinitystones.timestone.utils.time_utils import get_future_time
from .exceptions import TimestoneAPIError


class TimestoneClient:
    def __init__(self, base_url: str =None, auth_token: str =None, phone_number_id: str =None):
        self.settings = Settings()
        self.base_url = base_url or self.settings.BASE_URL
        self.auth_token = auth_token
        self.phone_number_id = phone_number_id
        self.timezone = self.settings.TIMEZONE

        if not self.auth_token:
            raise ValueError("WhatsApp auth token not configured")
        if not self.phone_number_id:
            raise ValueError("WhatsApp phone number ID not configured")

    def schedule_message(self, phone_number: str, message_data: dict[str, str], schedule_time: datetime =None):
        """Schedule a WhatsApp message"""
        if schedule_time is None:
            schedule_time = get_future_time(minutes=2)

        payload = {
            "schedule_time": schedule_time.isoformat(),
            "phone_number": phone_number,
            "message_data": message_data,
            "auth_token": self.auth_token,
            "phone_number_id": self.phone_number_id
        }

        try:
            response = requests.post(
                f"{self.base_url}/schedule-message",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TimestoneAPIError(f"Failed to schedule message: {str(e)}")

    def get_scheduled_messages(self):
        """Get all scheduled messages"""
        try:
            response = requests.get(
                f"{self.base_url}/scheduled-messages",
                params={"timezone": self.timezone}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TimestoneAPIError(f"Failed to fetch scheduled messages: {str(e)}")