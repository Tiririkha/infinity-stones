from .core import TimestoneCore
from .models import (
    ScheduledNotification,
    PaginatedResponse,
    TimedNotificationType,
    TimedNotificationStatus
)
from .exceptions import (
    TimestoneError,
    TimestoneAuthError,
    TimestoneAPIError,
    TimestoneConnectionError,
    TimestoneNotFoundError
)

# Version of the timestone package
__version__ = "0.1.0"

# All public classes and constants available when importing timestone
__all__ = [
    # Main API Client
    'TimestoneCore',

    # Models
    'ScheduledNotification',
    'PaginatedResponse',

    # Constants/Enums
    'TimedNotificationType',
    'TimedNotificationStatus',

    # Exceptions
    'TimestoneError',
    'TimestoneAuthError',
    'TimestoneAPIError',
    'TimestoneConnectionError',
    'TimestoneNotFoundError',
]

# Meta information about the package
__author__ = "Eric Kweyunga"
__author_email__ = "maverickweyunga@gmail.com"
__description__ = "Python client for Timestone notification service"
__url__ = "https://github.com/Tiririkha/infinity-stones"