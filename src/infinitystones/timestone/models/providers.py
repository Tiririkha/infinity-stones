from typing import Dict, List

from .base import BaseTModel, BaseResponseModel
from .enums import NotificationType


class NotificationProvider(BaseTModel):
    """Model representing a notification provider"""
    name: str
    provider_type: NotificationType
    configuration: Dict = None
    is_active: bool = True
    priority: int = 0
    rate_limit: int = 0
    failure_threshold: int = 5


class ProviderResponse(BaseResponseModel):
    """Paginated response for providers"""
    results: List[NotificationProvider]