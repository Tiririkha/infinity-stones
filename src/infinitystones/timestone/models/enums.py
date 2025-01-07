from enum import Enum

class NotificationType(str, Enum):
    """Notification types based on database model choices"""
    EMAIL = 'email'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'
    PUSH = 'push'

    @classmethod
    def choices(cls):
        """Get choices tuples as defined in database model"""
        return [
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp'),
            ('push', 'Push Notification'),
        ]


class NotificationStatus(str, Enum):
    """Notification statuses based on database model choices"""
    PENDING = 'pending'
    SCHEDULED = 'scheduled'
    PROCESSING = 'processing'
    SENT = 'sent'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

    @classmethod
    def choices(cls):
        """Get choices tuples as defined in database model"""
        return [
            ('pending', 'Pending'),
            ('scheduled', 'Scheduled'),
            ('processing', 'Processing'),
            ('sent', 'Sent'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ]


class ProviderType(str, Enum):
    """Provider types based on database model choices"""
    EMAIL = 'email'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'
    PUSH = 'push'

    @classmethod
    def choices(cls):
        """Get choices tuples as defined in database model"""
        return [
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp'),
            ('push', 'Push Notification'),
        ]