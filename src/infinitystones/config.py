import os
from functools import lru_cache
from typing import Optional
from uuid import UUID
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, model_validator

from dotenv import load_dotenv

load_dotenv()


class TimestoneConfigError(Exception):
    """Base exception for Timestone configuration errors"""
    pass


class MissingAPIKeyError(TimestoneConfigError):
    """Raised when API key is not provided"""

    def __init__(self):
        super().__init__(
            "Timestone API key not found. Please set TIMESTONE_API_KEY environment "
            "variable or provide it directly when initializing the client."
        )


class InvalidAPIKeyError(TimestoneConfigError):
    """Raised when API key is invalid"""

    def __init__(self):
        super().__init__(
            "Invalid API key format. Please provide a valid API key."
        )


class TimestoneSettings(BaseSettings):
    """Base configuration settings for infinitystones package"""
    model_config = SettingsConfigDict(
        env_prefix="TIMESTONE_",
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_assignment=True
    )

    # API Configuration
    API_KEY: str = Field(default="", description="Timestone API authentication key")
    BASE_URL: str = Field(
        default="http://localhost:8000/api/",
        description="Base URL for Timestone API",
        pattern="^https?://.*"  # Validate URL format
    )
    TIMEOUT: int = Field(
        default=10,
        description="Request timeout in seconds",
        ge=1,
        le=300
    )

    # Client Configuration
    MAX_RETRIES: int = Field(
        default=1,
        description="Maximum number of retry attempts",
        ge=0,
        le=10
    )
    RETRY_BACKOFF: float = Field(
        default=1.0,
        description="Exponential backoff factor",
        ge=0.1,
        le=60.0
    )
    POOL_CONNECTIONS: int = Field(
        default=10,
        description="Number of connection pools",
        ge=1,
        le=100
    )
    POOL_MAXSIZE: int = Field(
        default=10,
        description="Maximum pool size",
        ge=1,
        le=100
    )

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(
        default=True,
        description="Enable/disable rate limiting"
    )
    RATE_LIMIT_CALLS: int = Field(
        default=100,
        description="Maximum API calls per period",
        ge=1
    )
    RATE_LIMIT_PERIOD: int = Field(
        default=60,
        description="Rate limit period in seconds",
        ge=1
    )

    @field_validator("API_KEY")
    def validate_api_key(cls, v: str) -> str:
        """Validate API key is provided and is a valid UUID"""
        if not v:
            raise MissingAPIKeyError()

        try:
            UUID(v)
            return v
        except ValueError:
            raise InvalidAPIKeyError()

    @model_validator(mode='after')
    def validate_rate_limit_settings(self) -> 'TimestoneSettings':
        """Validate rate limit settings consistency"""
        if self.RATE_LIMIT_ENABLED:
            if self.RATE_LIMIT_CALLS < 1:
                raise ValueError("Rate limit calls must be greater than 0 when rate limiting is enabled")
            if self.RATE_LIMIT_PERIOD < 1:
                raise ValueError("Rate limit period must be greater than 0 when rate limiting is enabled")
        return self

    @model_validator(mode='after')
    def validate_pool_settings(self) -> 'TimestoneSettings':
        """Validate pool settings consistency"""
        if self.POOL_MAXSIZE < self.POOL_CONNECTIONS:
            raise ValueError("Pool maxsize must be greater than or equal to pool connections")
        return self


class TimestoneConfig:
    """Configuration manager for Timestone client"""

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            **kwargs
    ):
        """Initialize configuration with optional overrides"""
        settings_dict = get_settings().model_dump()

        # Update settings with provided values
        if api_key:
            settings_dict['API_KEY'] = api_key
        if base_url:
            settings_dict['BASE_URL'] = base_url
        settings_dict.update({k.upper(): v for k, v in kwargs.items()})

        # Create new settings instance with updated values
        # This will automatically validate all settings
        self._settings = TimestoneSettings(**settings_dict)

    @property
    def settings(self) -> TimestoneSettings:
        """Get current settings"""
        return self._settings

    def update(self, **kwargs):
        """Update settings with validation"""
        settings_dict = self._settings.model_dump()
        settings_dict.update({k.upper(): v for k, v in kwargs.items()})
        self._settings = TimestoneSettings(**settings_dict)


@lru_cache()
def get_settings() -> TimestoneSettings:
    """Get cached settings instance"""
    return TimestoneSettings()


settings = get_settings()
