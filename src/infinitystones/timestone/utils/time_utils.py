from datetime import datetime, timedelta
import pytz
from infinitystones.timestone.config.settings import Settings

settings = Settings()

def get_future_time(minutes=2):
    """Get a future time in the configured timezone"""
    tz = pytz.timezone(settings.TIMEZONE)
    return datetime.now(tz) + timedelta(minutes=minutes)

def format_datetime(dt):
    """Format datetime to ISO format with timezone"""
    if not dt.tzinfo:
        tz = pytz.timezone(settings.TIMEZONE)
        dt = tz.localize(dt)
    return dt.isoformat()