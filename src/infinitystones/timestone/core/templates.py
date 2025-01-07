from typing import Optional, Dict
from uuid import UUID

from .base import BaseCore, PaginatedListMixin
from ..models.templates import NotificationTemplate, TemplateResponse
from ..models.enums import NotificationType


class TemplateCore(BaseCore, PaginatedListMixin):
    """Core functionality for managing notification templates"""

    def list(
            self,
            notification_type: Optional[NotificationType] = None,
            is_active: Optional[bool] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None,
    ) -> TemplateResponse:
        """List templates with filtering"""
        params = {
            "type": notification_type.value if notification_type else None,
            "is_active": str(is_active).lower() if is_active is not None else None
        }
        response = self._get_paginated_results("/templates/", params, page, page_size)
        return TemplateResponse(**response)

    def get(self, id: UUID) -> NotificationTemplate:
        """Get template by ID"""
        response = self._request("GET", f"/templates/{id}/")
        return NotificationTemplate(**response)

    def create(
            self,
            name: str,
            notification_type: NotificationType,
            content_template: str,
            subject_template: Optional[str] = None,
            metadata: Optional[Dict] = None,
    ) -> NotificationTemplate:
        """Create a template"""
        data = {
            "name": name,
            "notification_type": notification_type.value,
            "content_template": content_template,
            "subject_template": subject_template,
            "metadata": metadata or {},
        }
        response = self._request("POST", "/templates/", json=data)
        return NotificationTemplate(**response)

    def update(
            self,
            _id: UUID,
            content_template: Optional[str] = None,
            subject_template: Optional[str] = None,
            metadata: Optional[Dict] = None,
            is_active: Optional[bool] = None,
    ) -> NotificationTemplate:
        """Update a template"""
        data = {k: v for k, v in {
            "content_template": content_template,
            "subject_template": subject_template,
            "metadata": metadata,
            "is_active": is_active
        }.items() if v is not None}

        response = self._request("PATCH", f"/templates/{_id}/", json=data)
        return NotificationTemplate(**response)

    def delete(self, _id: UUID) -> None:
        """Delete a template"""
        self._request("DELETE", f"/templates/{_id}/")

    def validate(
            self,
            _id: UUID,
            template_data: Dict
    ) -> Dict:
        """Validate template with sample data"""
        response = self._request(
            "POST",
            f"/templates/{_id}/validate/",
            json={"data": template_data}
        )
        return response
