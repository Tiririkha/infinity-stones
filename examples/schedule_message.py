import os
import json
from infinitystones.timestone.client.api_client import TimestoneClient
from infinitystones.timestone.client.exceptions import TimestoneAPIError
from infinitystones.timestone.utils.time_utils import get_future_time

from dotenv import load_dotenv
load_dotenv()

def main():
    # Initialize client
    client = TimestoneClient(
        auth_token=os.getenv('WHATSAPP_AUTH_TOKEN'),
        phone_number_id=os.getenv('WHATSAPP_PHONE_ID')
    )

    # Test message details
    phone_number = "255**"
    message = {
        "type": "text",
        "text": {
            "body": "Hello! There"
        }
    }

    try:
        # Schedule a message
        result = client.schedule_message(
            phone_number=phone_number,
            message_data=message,
            schedule_time=get_future_time(minutes=0.1)
        )
        print("Schedule Result:", json.dumps(result, indent=2))

    except TimestoneAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()