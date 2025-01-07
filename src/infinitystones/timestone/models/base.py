from typing import Optional, Dict
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseTModel(BaseModel):
    """Base model for all API models"""
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    id: UUID
    created_at: datetime
    updated_at: datetime


class BaseResponseModel(BaseModel):
    """Base model for paginated responses"""
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None