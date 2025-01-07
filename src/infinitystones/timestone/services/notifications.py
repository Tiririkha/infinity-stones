import uuid
from typing import List, Optional, Dict, Union
from datetime import datetime, timedelta
from uuid import UUID

from infinitystones.timestone.client import TimestoneClient
from infinitystones.timestone.models.enums import NotificationType, NotificationStatus
from infinitystones.timestone.models.notifications import (
    ScheduledNotification,
    NotificationLog,
    NotificationResponse
)


class NotificationService(TimestoneClient):
    def list_notifications(
            self,
            status: Optional[NotificationStatus] = None,
            notification_type: Optional[NotificationType] = None,
            scheduled_after: Optional[datetime] = None,
            scheduled_before: Optional[datetime] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None
    ) -> NotificationResponse:
        params = {k: v for k, v in {
            "status": getattr(status, 'value', None),
            "type": getattr(notification_type, 'value', None),
            "scheduled_after": scheduled_after.isoformat() if scheduled_after else None,
            "scheduled_before": scheduled_before.isoformat() if scheduled_before else None,
            "page": page,
            "page_size": page_size
        }.items() if v is not None}

        response = self._request("GET", "/notifications/", params=params)
        return NotificationResponse(**response)

    def create_notification(
            self,
            notification_type: NotificationType,
            scheduled_time: Union[str, datetime] = None,
            recipient_timezone: str = "UTC",
            subject: str = '',
            template: Optional[str] = None,
            recipient_email: Optional[str] = None,
            recipient_phone: Optional[str] = None,
            recipient_id: Optional[str] = None,
            metadata: Optional[Dict] = None,
    ) -> ScheduledNotification:
        if scheduled_time is None:
            scheduled_time = datetime.now().astimezone()
        elif isinstance(scheduled_time, str):
            scheduled_time = datetime.fromisoformat(scheduled_time)

        data = {k: v for k, v in {
            "notification_type": notification_type.value,
            "content": template,
            "scheduled_time": scheduled_time.isoformat(),
            "recipient_timezone": recipient_timezone,
            "subject": subject,
            "template": template,
            "recipient_email": recipient_email,
            "recipient_phone": recipient_phone,
            "recipient_id": recipient_id,
            "metadata": metadata,
            "idempotency_key": self._generate_idempotency_key()
        }.items() if v is not None}

        response = self._request("POST", "/notifications/", json=data)
        return ScheduledNotification(**response)

    def get_notification(self, notification_id: Union[UUID, str]) -> ScheduledNotification:
        notification_id = str(notification_id)
        response = self._request("GET", f"/notifications/{notification_id}/")
        return ScheduledNotification(**response)

    def cancel_notification(self, notification_id: Union[UUID, str]) -> ScheduledNotification:
        notification_id = str(notification_id)
        response = self._request("POST", f"/notifications/{notification_id}/cancel/")
        return ScheduledNotification(**response)

    @staticmethod
    def schedule_for(
            year: int,
            month: int,
            day: int,
            hour: int = 0,
            minute: int = 0,
            second: int = 0,
            microsecond: int = 0,
    ) -> str:
        schedule_time = datetime(year, month, day, hour, minute, second, microsecond)
        if schedule_time <= datetime.now() + timedelta(minutes=1):
            raise ValueError("Schedule time must be at least 1 minute in the future")
        return schedule_time.astimezone().isoformat()

    @staticmethod
    def _generate_idempotency_key() -> str:
        return str(uuid.uuid4())
