# WhatsApp Message Scheduler Documentation

## Overview
This Python script enables scheduling WhatsApp messages using the Infinity Stones Timestone client. It provides functionality to send delayed messages through the WhatsApp Business API.

## Prerequisites
- Python 3.x
- Required Python packages:
  - `infinitystones.timestone`
  - `python-dotenv`
- WhatsApp Business API credentials
  - Auth Token
  - Phone Number ID

## Environment Setup

### Environment Variables
The script requires two environment variables to be set in a `.env` file:
```
WHATSAPP_AUTH_TOKEN=your_auth_token_here
WHATSAPP_PHONE_ID=your_phone_number_id_here
```

### Installation
```bash
pip install infinitystones-timestone python-dotenv
```

## Code Structure

### Imports
```python
import os
import json
from infinitystones.timestone.client.api_client import TimestoneClient
from infinitystones.timestone.client.exceptions import TimestoneAPIError
from infinitystones.timestone.utils.time_utils import get_future_time
from dotenv import load_dotenv
```

### Main Components

1. **Environment Configuration**
   ```python
   load_dotenv()
   ```
   Loads environment variables from the `.env` file.

2. **Client Initialization**
   ```python
   client = TimestoneClient(
       auth_token=os.getenv('WHATSAPP_AUTH_TOKEN'),
       phone_number_id=os.getenv('WHATSAPP_PHONE_ID')
   )
   ```
   Creates a new instance of the TimestoneClient with authentication credentials.

3. **Message Configuration**
   ```python
   message = {
       "type": "text",
       "text": {
           "body": "Habari Eric, hii ni jaribio la ujumbe wa WhatsApp kutoka kwa Infinity Stones"
       }
   }
   ```
   Defines the message structure with Swahili text content.

## Function Reference

### schedule_message()
Schedules a WhatsApp message for future delivery.

**Parameters:**
- `phone_number` (str): Recipient's phone number
- `message_data` (dict): Message content and type
- `schedule_time` (datetime): Delivery time, generated using `get_future_time()`

**Returns:**
- JSON response containing scheduling details

### get_future_time()
Utility function to calculate future timestamp.

**Parameters:**
- `minutes` (int): Number of minutes in the future

**Returns:**
- DateTime object representing the future time

## Error Handling
The script implements two levels of error handling:

1. **API-specific errors**
   ```python
   except TimestoneAPIError as e:
       print(f"API Error: {e}")
   ```
   Catches errors related to the Timestone API.

2. **General exceptions**
   ```python
   except Exception as e:
       print(f"Unexpected error: {e}")
   ```
   Catches any other unexpected errors.

## Usage Example
```python
def main():
    client = TimestoneClient(
        auth_token=os.getenv('WHATSAPP_AUTH_TOKEN'),
        phone_number_id=os.getenv('WHATSAPP_PHONE_ID')
    )
    
    result = client.schedule_message(
        phone_number="255**",
        message_data={
            "type": "text",
            "text": {
                "body": "Your message here"
            }
        },
        schedule_time=get_future_time(minutes=50)
    )
```

## Best Practices
1. Always store sensitive credentials in environment variables
2. Implement proper error handling for both API and general errors
3. Validate phone numbers before sending messages
4. Monitor API responses for successful message scheduling
5. Use try-except blocks to handle potential errors gracefully

## Limitations
- Phone numbers must be in the correct format with country code
- Message scheduling is subject to WhatsApp Business API limits
- Authentication tokens must be valid and not expired

## Security Considerations
1. Never hard-code authentication credentials
2. Store the `.env` file securely and add it to `.gitignore`
3. Regularly rotate authentication tokens
4. Validate and sanitize phone numbers and message content
5. Monitor for failed authentication attempts

## Troubleshooting
Common issues and solutions:

1. **Authentication Errors**
   - Verify environment variables are correctly set
   - Check if auth token is valid and not expired
   - Ensure phone number ID is correct

2. **Scheduling Errors**
   - Verify recipient phone number format
   - Check if schedule time is valid
   - Ensure message format follows WhatsApp API requirements

3. **API Connection Issues**
   - Check internet connectivity
   - Verify API endpoint availability
   - Confirm firewall settings allow API connections