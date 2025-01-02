class TimestoneError(Exception):
    """Base exception for Timestone client"""
    pass

class TimestoneAuthError(TimestoneError):
    """Authentication error"""
    pass

class TimestoneAPIError(TimestoneError):
    """API error"""
    pass

class TimestoneConnectionError(TimestoneError):
    """Connection error"""
    pass

class TimestoneNotFoundError(TimestoneError):
    """Resource not found error"""
    pass

#  WhatsApp sender exceptions
class WhatsAppSenderError(Exception):
   """Base exception for WhatsApp sender validation"""
   pass

class InvalidWhatsAppTokenError(WhatsAppSenderError):
   """Invalid WhatsApp token error"""
   pass

class InvalidPhoneNumberIDError(WhatsAppSenderError):
   """Invalid phone number ID error"""
   pass

class WhatsAppAPIError(WhatsAppSenderError):
   """WhatsApp API error"""
   pass