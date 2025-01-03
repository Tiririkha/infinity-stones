from dotenv.main import logger

from .exceptions import InvalidPhoneNumberIDError, InvalidWhatsAppTokenError, WhatsAppAPIError
from .models import WhatsAppSender


class UseTimedNotification:
    def initialize(self):
        raise NotImplementedError("Notifiers must implement this method")

class UseWhatsAppTimedNotification(UseTimedNotification):
    def __init__(self, wa_token: str, wa_phone_number_id: str):
        self.wa_token = wa_token
        self.wa_phone_number_id = wa_phone_number_id

    def get_json(self):
        return {
            "wa_token": self.wa_token,
            "wa_phone_number_id": self.wa_phone_number_id
        }

    def initialize(self):
        try:
            sender = WhatsAppSender(
                wa_token=self.wa_token,
                wa_phone_number_id=self.wa_phone_number_id
            )
            return sender
        except InvalidPhoneNumberIDError as e:
            logger.error(f"Phone number validation failed: {str(e)}")
            raise InvalidPhoneNumberIDError("Failed to initialize WhatsApp sender - check your phone number ID value")
        except InvalidWhatsAppTokenError as e:
            logger.error(f"Token validation failed: {str(e)}")
            raise InvalidWhatsAppTokenError("Failed to initialize WhatsApp sender - check your token value")
        except WhatsAppAPIError as e:
            logger.error(f"WhatsApp API error: {str(e)}")
            raise WhatsAppAPIError("Failed to initialize WhatsApp sender, check your token and phone number ID values")
