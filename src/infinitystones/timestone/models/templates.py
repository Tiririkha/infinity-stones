from typing import Optional, Dict, List

from .base import BaseTModel, BaseResponseModel
from .enums import NotificationType


class NotificationTemplate(BaseTModel):
    """Model representing a notification template"""
    name: str
    notification_type: NotificationType
    subject_template: Optional[str] = None
    content_template: str
    metadata: Dict = None
    is_active: bool = True


class TemplateResponse(BaseResponseModel):
    """Paginated response for templates"""
    results: List[NotificationTemplate]