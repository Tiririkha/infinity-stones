from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID

from .base import BaseTModel, BaseResponseModel
from .enums import NotificationType, NotificationStatus


class ScheduledNotification(BaseTModel):
    """Model representing a scheduled notification"""
    notification_type: NotificationType
    subject: Optional[str] = None
    content: str
    template: Optional[str] = None

    # Recipient details
    recipient_email: Optional[str] = None
    recipient_phone: Optional[str] = None
    recipient_id: Optional[str] = None

    # Scheduling
    scheduled_time: datetime
    recipient_timezone: str = "UTC"

    # Status and delivery
    status: NotificationStatus = NotificationStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    last_attempt: Optional[datetime] = None
    next_retry_at: Optional[datetime] = None

    # Additional data
    metadata: Dict = None
    idempotency_key: Optional[UUID] = None
    provider_response: Dict = None


class NotificationResponse(BaseResponseModel):
    """Paginated response for notifications"""
    results: List[ScheduledNotification]