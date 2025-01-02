import json
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer
import requests
import logging

from .exceptions import WhatsAppAPIError, InvalidWhatsAppTokenError, InvalidPhoneNumberIDError

logger = logging.getLogger(__name__)


class TimedNotificationType:
    EMAIL = "email"
    SMS = "sms"
    BOTH = "both"
    WHATSAPP = "whatsapp"


class TimedNotificationStatus:
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class WhatsAppSender(BaseModel):
    wa_token: str
    wa_phone_number_id: str

    @field_validator("wa_phone_number_id")
    def validate_wa_phone_number_id(cls, value):
        if not value.strip():
            raise InvalidPhoneNumberIDError("WhatsApp phone number ID cannot be empty")
        if not value.isdigit():
            raise InvalidPhoneNumberIDError("WhatsApp phone number ID must contain only digits")
        return value

    @field_validator("wa_token")
    def validate_wa_token(cls, value):
        if not value.strip():
            raise InvalidWhatsAppTokenError("WhatsApp token cannot be empty")

        try:
            response = requests.get(
                f"https://graph.facebook.com/v17.0/me",
                params={"access_token": value},
                timeout=5
            )

            if response.status_code == 401:
                raise InvalidWhatsAppTokenError("Invalid WhatsApp token - authentication failed")

            response.raise_for_status()
            data = response.json()

            if "id" not in data:
                raise WhatsAppAPIError("Invalid response from WhatsApp API - check your token value")

        except requests.Timeout:
            raise WhatsAppAPIError("WhatsApp API request timed out")
        except requests.ConnectionError:
            raise WhatsAppAPIError("Failed to connect to WhatsApp API")
        except requests.RequestException as e:
            raise WhatsAppAPIError(f"WhatsApp API error: {str(e)}")

        return value

    @field_serializer('wa_token')
    def serialize_token(self, value):
        return str(value)

    @field_serializer('wa_phone_number_id')
    def serialize_phone_id(self, value):
        return str(value)

    def model_dump_json(self, *args, **kwargs):
        return json.dumps({
            "wa_token": self.wa_token,
            "wa_phone_number_id": self.wa_phone_number_id
        })

    class Config:
        json_encoders = {
            'wa_token': str,
            'wa_phone_number_id': str
        }

class ScheduledNotification(BaseModel):
    id: Optional[int] = None
    notification_type: str = Field(..., description="Type of notification: email, sms, or both")
    subject: Optional[str] = Field(None, max_length=200)
    content: str
    recipient_email: Optional[EmailStr] = Field(None, max_length=254)
    recipient_phone: Optional[str] = Field(None, max_length=15)
    scheduled_time: str = Field(..., description="ISO 8601 format with timezone")
    local_scheduled_time: Optional[str] = None
    recipient_timezone: str
    wa: Optional[WhatsAppSender] = None
    webhook_url: Optional[str] = None
    status: Optional[str] = None
    metadata: Dict = Field(default=dict)
    created_at: Optional[datetime] = None


class PaginatedResponse(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[ScheduledNotification]

