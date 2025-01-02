from infinitystones.timestone.config import config
from typing import List, Optional, Dict, Union
from datetime import datetime
from .client import TimestoneClient
from .models import (
    ScheduledNotification,
    PaginatedResponse,
    TimedNotificationType,
    WhatsAppSender
)


class TimestoneCore(TimestoneClient):
    def __init__(self):
        super().__init__(
            timeout=int(config.TIMESTONE_TIMEOUT)
        )

    def list_notifications(
            self,
            search: Optional[str] = None,
            ordering: Optional[str] = None,
            page: Optional[int] = None
    ) -> PaginatedResponse:
        """Get list of notifications with optional filtering and pagination."""
        params = {
            "search": search,
            "ordering": ordering,
            "page": page
        }
        response = self._request("GET", "/notifications/", params=params)
        return PaginatedResponse(**response)

    def create_timed_notification(
            self,
            notification_type: TimedNotificationType,
            content: str,
            scheduled_time: Union[str, datetime],
            recipient_timezone: str,
            wa: Optional[WhatsAppSender] = None,
            webhook_url: Optional[str] = None,
            subject: Optional[str] = None,
            recipient_email: Optional[str] = None,
            recipient_phone: Optional[str] = None,
            metadata: Optional[Dict] = None,
    ) -> ScheduledNotification:
        """Create a new notification."""
        if isinstance(scheduled_time, datetime):
            scheduled_time = scheduled_time.isoformat()

        data = {
            "notification_type": notification_type,
            "content": content,
            "scheduled_time": scheduled_time,
            "recipient_timezone": recipient_timezone,
            "subject": subject,
            "wa": wa or {},
            "webhook_url": webhook_url,
            "recipient_email": recipient_email,
            "recipient_phone": recipient_phone,
            "metadata": metadata or {}
        }
        response = self._request("POST", "/notifications/", json=data)
        return ScheduledNotification(**response)

    def bulk_create_timed_notifications(
            self,
            notifications: List[Dict]
    ) -> List[ScheduledNotification]:
        """Create multiple notifications in bulk."""
        response = self._request("POST", "/notifications/bulk_create/", json=notifications)
        return [ScheduledNotification(**item) for item in response]

    def get_timed_notification(self, notification_id: int) -> ScheduledNotification:
        """Get a specific notification by ID."""
        response = self._request("GET", f"/notifications/{notification_id}/")
        return ScheduledNotification(**response)

    def update_timed_notification(
            self,
            notification_id: int,
            **update_data
    ) -> ScheduledNotification:
        """Update a notification."""
        response = self._request(
            "PATCH",
            f"/notifications/{notification_id}/",
            json=update_data
        )
        return ScheduledNotification(**response)

    def delete_timed_notification(self, notification_id: int) -> None:
        """Delete a notification."""
        self._request("DELETE", f"/notifications/{notification_id}/")

    def get_notification_local_time(
            self,
            notification_id: int
    ) -> Dict[str, str]:
        """Get notification time in local timezone."""
        return self._request("GET", f"/notifications/{notification_id}/local_time/")

    def get_available_timezones(self) -> List[str]:
        """Get list of available timezones."""
        return self._request("GET", "/notifications/timezones/")

    @staticmethod
    def notifyAT(
            self,
            year: int,
            month: int,
            day: int,
            hour: Optional[int] = 0,
            minute: Optional[int] = 0,
            second: Optional[int] = 0,
            microsecond: Optional[int] = 0,
    ) -> str:
        """Convert a datetime to ISO 8601 format."""
        return datetime(
            year, month, day, hour, minute, second, microsecond
        ).astimezone().isoformat()
