from datetime import datetime, timedelta
import pytz
from infinitystones.timestone.config.settings import Settings

settings = Settings()

def get_future_time(minutes: float =2):
    """Get a future time in the configured timezone"""
    tz = pytz.timezone(settings.TIMEZONE)
    return datetime.now(tz) + timedelta(minutes=minutes)

def format_datetime(dt: datetime):
    """Format datetime to ISO format with timezone"""
    if not dt.tzinfo:
        tz = pytz.timezone(settings.TIMEZONE)
        dt = tz.localize(dt)
    return dt.isoformat()

def set_future_time(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0
):
    """Set a future time in the configured timezone"""
    tz = pytz.timezone(settings.TIMEZONE)
    return tz.localize(datetime(year, month, day, hour, minute, second, microsecond))