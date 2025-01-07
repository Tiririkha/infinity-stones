from typing import Optional, Dict
from uuid import UUID

from infinitystones.timestone.client import TimestoneClient
from infinitystones.timestone.models.enums import ProviderType
from infinitystones.timestone.models.providers import NotificationProvider, ProviderResponse


class ProviderService(TimestoneClient):
    """Service for managing notification providers"""

    def list_providers(
            self,
            provider_type: Optional[ProviderType] = None,
            is_active: Optional[bool] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None,
    ) -> ProviderResponse:
        """List notification providers with filtering"""
        params = {
            "type": provider_type.value if provider_type else None,
            "is_active": str(is_active).lower() if is_active is not None else None,
            "page": page,
            "page_size": page_size
        }
        response = self._request("GET", "/providers/", params=params)
        return ProviderResponse(**response)

    def create_provider(
            self,
            name: str,
            provider_type: ProviderType,
            configuration: Dict,
            priority: int = 0,
            rate_limit: int = 0,
            failure_threshold: int = 5,
    ) -> NotificationProvider:
        """Create a notification provider"""
        data = {
            "name": name,
            "provider_type": provider_type.value,
            "configuration": configuration,
            "priority": priority,
            "rate_limit": rate_limit,
            "failure_threshold": failure_threshold,
        }
        response = self._request("POST", "/providers/", json=data)
        return NotificationProvider(**response)

    def get_provider(self, provider_id: UUID) -> NotificationProvider:
        """Get provider details"""
        response = self._request("GET", f"/providers/{provider_id}/")
        return NotificationProvider(**response)

    def update_provider(
            self,
            provider_id: UUID,
            configuration: Optional[Dict] = None,
            priority: Optional[int] = None,
            rate_limit: Optional[int] = None,
            failure_threshold: Optional[int] = None,
            is_active: Optional[bool] = None,
    ) -> NotificationProvider:
        """Update a provider"""
        data = {k: v for k, v in {
            "configuration": configuration,
            "priority": priority,
            "rate_limit": rate_limit,
            "failure_threshold": failure_threshold,
            "is_active": is_active
        }.items() if v is not None}

        response = self._request("PATCH", f"/providers/{provider_id}/", json=data)
        return NotificationProvider(**response)

    def delete_provider(self, provider_id: UUID) -> None:
        """Delete a provider"""
        self._request("DELETE", f"/providers/{provider_id}/")

    def test_provider(
            self,
            provider_id: UUID,
            test_data: Optional[Dict] = None
    ) -> Dict:
        """Test provider configuration"""
        response = self._request(
            "POST",
            f"/providers/{provider_id}/test/",
            json=test_data or {}
        )
        return response
