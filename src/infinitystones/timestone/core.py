from infinitystones.timestone.config import config
from typing import List, Optional, Dict, Union, NotRequired, TypedDict
from datetime import datetime, timedelta
from .client import TimestoneClient
from .models import (
    ScheduledNotification,
    PaginatedResponse,
    TimedNotificationType,
)


class NotificationData(TypedDict):
    notification_type: TimedNotificationType
    content: str
    scheduled_time: Union[str, datetime]
    recipient_timezone: str
    wa: NotRequired[Optional[dict]]
    webhook_url: NotRequired[Optional[str]]
    subject: NotRequired[Optional[str]]
    recipient_email: NotRequired[Optional[str]]
    recipient_phone: NotRequired[Optional[str]]
    metadata: NotRequired[Optional[Dict]]


class TimestoneCore(TimestoneClient):
    """TimestoneCore handles scheduling and managing timed notifications."""

    def __init__(self):
        super().__init__(timeout=int(config.TIMESTONE_TIMEOUT))

    def list_notifications(
            self,
            search: Optional[str] = None,
            ordering: Optional[str] = None,
            page: Optional[int] = None
    ) -> PaginatedResponse:
        """Get paginated list of notifications with optional filtering."""
        params = {"search": search, "ordering": ordering, "page": page}
        response = self._request("GET", "/notifications/", params=params)
        return PaginatedResponse(**response)

    def create_timed_notification(
            self,
            notification_type: TimedNotificationType,  # Required
            content: str,  # Required
            scheduled_time: Union[str, datetime],  # Required
            recipient_timezone: str,  # Required
            wa: Optional[dict] = None,
            webhook_url: Optional[str] = None,
            subject: Optional[str] = None,
            recipient_email: Optional[str] = None,
            recipient_phone: Optional[str] = None,
            metadata: Optional[Dict] = None,
    ) -> ScheduledNotification:
        """Create a new timed notification."""
        if isinstance(scheduled_time, datetime):
            scheduled_time = scheduled_time.isoformat()

        data = {
            "notification_type": notification_type,
            "content": content,
            "scheduled_time": scheduled_time,
            "recipient_timezone": recipient_timezone,
            "subject": subject or None,
            "wa": wa or None,
            "webhook_url": webhook_url or None,
            "recipient_email": recipient_email or None,
            "recipient_phone": recipient_phone or None,
            "metadata": metadata or {}
        }
        response = self._request("POST", "/notifications/", json=data)
        return ScheduledNotification(**response)

    def bulk_create_timed_notifications(
            self,
            notifications: List[NotificationData]
    ) -> List[ScheduledNotification]:
        """Create multiple notifications in bulk."""
        response = self._request("POST", "/notifications/bulk_create/", json=notifications)
        return [ScheduledNotification(**item) for item in response]

    def get_timed_notification(
            self,
            notification_id: int
    ) -> ScheduledNotification:
        """Get a specific notification by ID."""
        response = self._request("GET", f"/notifications/{notification_id}/")
        return ScheduledNotification(**response)

    def update_timed_notification(
            self,
            notification_id: int,
            **update_data: NotificationData
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

    def get_notification_local_time(self, notification_id: int) -> Dict[str, str]:
        """Get notification time in local timezone."""
        return self._request("GET", f"/notifications/{notification_id}/local_time/")

    def get_available_timezones(self) -> List[str]:
        """Get list of supported timezone names."""
        return self._request("GET", "/notifications/timezones/")

    @staticmethod
    def notifyAT(
            year: int,
            month: int,
            day: int,
            hour: int = 0,
            minute: int = 0,
            second: int = 0,
            microsecond: int = 0,
    ) -> str:
        """Convert date/time components to ISO 8601 string for scheduling."""
        notify_time = datetime(year, month, day, hour, minute, second, microsecond)
        current_time = datetime.now()

        if notify_time > current_time + timedelta(minutes=1):
            return notify_time.astimezone().isoformat()
        raise ValueError("Notification time must be at least 1 minute ahead of current time")