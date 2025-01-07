from abc import ABC, abstractmethod
from typing import Optional, Dict, List, TypeVar
from uuid import UUID

from ..client import TimestoneClient
from ..models.base import BaseResponseModel

T = TypeVar('T')


class BaseCore(TimestoneClient, ABC):
    """Abstract base core with common functionality"""

    @abstractmethod
    def list(self, *args, **kwargs) -> BaseResponseModel:
        """List resources"""
        pass

    @abstractmethod
    def get(self, _id: UUID) -> T:
        """Get a resource by ID"""
        pass

    @abstractmethod
    def create(self, *args, **kwargs) -> T:
        """Create a resource"""
        pass

    @abstractmethod
    def update(self, _id: UUID, **kwargs) -> T:
        """Update a resource"""
        pass

    @abstractmethod
    def delete(self, _id: UUID) -> None:
        """Delete a resource"""
        pass


class PaginatedListMixin(TimestoneClient):
    """Mixin for paginated list operations"""

    def _get_paginated_results(
            self,
            endpoint: str,
            params: Optional[Dict] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None
    ) -> Dict:
        """Get paginated results with optional filtering"""
        params = params or {}
        if page:
            params['page'] = page
        if page_size:
            params['page_size'] = page_size
        return self._request("GET", endpoint, params=params)


class BulkOperationsMixin(TimestoneClient):
    """Mixin for bulk operations"""

    def _bulk_create(
            self,
            endpoint: str,
            items: List[Dict]
    ) -> List[Dict]:
        """Perform bulk create operation"""
        return self._request("POST", f"{endpoint}/bulk/", json=items)

    def _bulk_update(
            self,
            endpoint: str,
            items: List[Dict]
    ) -> List[Dict]:
        """Perform bulk update operation"""
        return self._request("PATCH", f"{endpoint}/bulk/", json=items)

    def _bulk_delete(
            self,
            endpoint: str,
            ids: List[UUID]
    ) -> None:
        """Perform bulk delete operation"""
        self._request("DELETE", f"{endpoint}/bulk/", json={"ids": [str(id) for id in ids]})
