import logging
import os
from dataclasses import dataclass

import pytz
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class Settings:
    BASE_URL: str = os.getenv('TIMESTONE_BASE_URL', 'http://127.0.0.1:8080')
    TIMEZONE: str = os.getenv('TIMEZONE', 'Africa/Dar_es_Salaam')

    def __post_init__(self):
        # Validate settings
        if (not os.getenv('TIMEZONE')
            or not isinstance(self.TIMEZONE, str)
            or len(self.TIMEZONE) == 0
            or self.TIMEZONE.isspace()) \
                or self.TIMEZONE not in pytz.all_timezones:
            logging.warning("Timezone not configured, defaulting to Africa/Dar_es_Salaam")
