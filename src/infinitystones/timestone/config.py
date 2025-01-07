from typing import Optional

from pydantic import BaseModel


class TimestoneConfig(BaseModel):
    """Configuration for Timestone client"""

    api_key: str
    base_url: str
    timeout: int
    max_retries: int = 1
    retry_backoff: float = 1.0
    pool_connections: int = 10
    pool_maxsize: int = 10

    @classmethod
    def from_settings(cls, api_key: Optional[str] = None) -> "TimestoneConfig":
        """Create config from global settings"""
        from infinitystones.config import settings

        return cls(
            api_key=api_key or settings.API_KEY,
            base_url=settings.BASE_URL,
            timeout=settings.TIMEOUT,
            max_retries=settings.MAX_RETRIES,
            retry_backoff=settings.RETRY_BACKOFF,
            pool_connections=settings.POOL_CONNECTIONS,
            pool_maxsize=settings.POOL_MAXSIZE,
        )

    def update(self, **kwargs) -> None:
        """Update config values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
