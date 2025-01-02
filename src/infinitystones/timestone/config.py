import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from infinitystones.config import config

load_dotenv()


class TimestoneConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("TIMESTONE_API_KEY", ""))
    base_url: str = Field(
        default=config.TIMESTONE_URL,
        description="Base URL for Timestone API"
    )
    timeout: int = Field(default=30, description="Request timeout in seconds")

    class Config:
        frozen = True
