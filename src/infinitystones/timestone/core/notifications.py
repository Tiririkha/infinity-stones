from typing import Optional, Dict, Union, List
from datetime import datetime
from uuid import UUID

from .base import BaseCore, PaginatedListMixin, BulkOperationsMixin
from ..models.notifications import (
    ScheduledNotification,
    NotificationLog,
    NotificationResponse
)
from ..models.enums import NotificationType, NotificationStatus


class NotificationCore(BaseCore, PaginatedListMixin, BulkOperationsMixin):
    """Core functionality for managing notifications"""

    def list(
            self,
            status: Optional[NotificationStatus] = None,
            notification_type: Optional[NotificationType] = None,
            scheduled_after: Optional[datetime] = None,
            scheduled_before: Optional[datetime] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None,
    ) -> NotificationResponse:
        """List notifications with filtering"""
        params = {
            "status": status.value if status else None,
            "type": notification_type.value if notification_type else None,
            "scheduled_after": scheduled_after.isoformat() if scheduled_after else None,
            "scheduled_before": scheduled_before.isoformat() if scheduled_before else None
        }
        response = self._get_paginated_results("/notifications/", params, page, page_size)
        return NotificationResponse(**response)

    def get(self, id: UUID) -> ScheduledNotification:
        """Get notification by ID"""
        response = self._request("GET", f"/notifications/{id}/")
        return ScheduledNotification(**response)

    def create(
            self,
            notification_type: NotificationType,
            content: str,
            scheduled_time: Union[str, datetime],
            recipient_timezone: str = "UTC",
            subject: Optional[str] = None,
            template_id: Optional[UUID] = None,
            template_data: Optional[Dict] = None,
            recipient_email: Optional[str] = None,
            recipient_phone: Optional[str] = None,
            recipient_id: Optional[str] = None,
            metadata: Optional[Dict] = None,
            max_retries: int = 3,
            idempotency_key: Optional[UUID] = None,
    ) -> ScheduledNotification:
        """Create a notification"""
        if isinstance(scheduled_time, datetime):
            scheduled_time = scheduled_time.isoformat()

        data = {
            "notification_type": notification_type.value,
            "content": content,
            "scheduled_time": scheduled_time,
            "recipient_timezone": recipient_timezone,
            "subject": subject,
            "template_id": str(template_id) if template_id else None,
            "template_data": template_data or {},
            "recipient_email": recipient_email,
            "recipient_phone": recipient_phone,
            "recipient_id": recipient_id,
            "metadata": metadata or {},
            "max_retries": max_retries,
            "idempotency_key": str(idempotency_key) if idempotency_key else None,
        }
        response = self._request("POST", "/notifications/", json=data)
        return ScheduledNotification(**response)

    def update(
            self,
            id: UUID,
            content: Optional[str] = None,
            scheduled_time: Optional[Union[str, datetime]] = None,
            recipient_timezone: Optional[str] = None,
            subject: Optional[str] = None,
            metadata: Optional[Dict] = None,
            max_retries: Optional[int] = None,
    ) -> ScheduledNotification:
        """Update a notification"""
        data = {k: v for k, v in {
            "content": content,
            "scheduled_time": scheduled_time.isoformat() if isinstance(scheduled_time, datetime) else scheduled_time,
            "recipient_timezone": recipient_timezone,
            "subject": subject,
            "metadata": metadata,
            "max_retries": max_retries
        }.items() if v is not None}

        response = self._request("PATCH", f"/notifications/{id}/", json=data)
        return ScheduledNotification(**response)

    def delete(self, id: UUID) -> None:
        """Delete a notification"""
        self._request("DELETE", f"/notifications/{id}/")

    def cancel(self, id: UUID) -> ScheduledNotification:
        """Cancel a scheduled notification"""
        response = self._request("POST", f"/notifications/{id}/cancel/")
        return ScheduledNotification(**response)

    def get_logs(
            self,
            _id: UUID,
            include_response_data: bool = False
    ) -> List[NotificationLog]:
        """Get notification delivery logs"""
        params = {"include_response": str(include_response_data).lower()}
        response = self._request("GET", f"/notifications/{_id}/logs/", params=params)
        return [NotificationLog(**log) for log in response]

    def bulk_create(self, notifications: List[Dict]) -> List[ScheduledNotification]:
        """Create multiple notifications"""
        response = self._bulk_create("/notifications", notifications)
        return [ScheduledNotification(**item) for item in response]

    def bulk_update(self, notifications: List[Dict]) -> List[ScheduledNotification]:
        """Update multiple notifications"""
        response = self._bulk_update("/notifications", notifications)
        return [ScheduledNotification(**item) for item in response]

    def bulk_delete(self, ids: List[UUID]) -> None:
        """Delete multiple notifications"""
        self._bulk_delete("/notifications", ids)

    def get_local_time(self, id: UUID) -> Dict[str, str]:
        """Get notification time in local timezone"""
        return self._request("GET", f"/notifications/{id}/local_time/")
