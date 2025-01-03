# Infinity Stones

A Python package providing powerful tools for real-world development challenges.

[![PyPI ](https://badge.fury.io/py/infinitystones.svg)](https://badge.fury.io/py/infinitystones)
[![GitHub](https://img.shields.io/github/license/Tiririkha/infinity-stones)](https://github.com/Tiririkha/infinity-stones/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://github.com/Tiririkha/infinity-stones)

## TimeStone

TimeStone is a notification scheduling and delivery system supporting:

- Email notifications
- SMS notifications  
- WhatsApp messages
- Webhook integration
- Custom metadata
- Timezone handling
- Bulk operations

### Installation

```bash
pip install infinitystones
```

### Quick Start

```python
from infinitystones.timestone import TimestoneCore, TimedNotificationType
from infinitystones.timestone.timed_notifications import UseWhatsAppTimedNotification
from infinitystones.timestone import TimestoneCore, TimedNotificationType

# Initialize client
client = TimestoneCore()

# Schedule an email notification
client.create_timed_notification(
    notification_type=TimedNotificationType.EMAIL,
    content="Meeting in 1 hour!",
    scheduled_time="2024-01-03T15:00:00Z",
    recipient_timezone="UTC",
    recipient_email="user@example.com"
)

# We can schedule whatsapp notifications as well

# Create a WhatsApp sender
whatsapp_sender = UseWhatsAppTimedNotification(
    wa_token="wa_token",
    wa_phone_number_id="wa_phone_number_id"
)

# Initialize whatsapp sender
whatsapp_sender.initialize()

# Configure WhatsApp message
client.create_timed_notification(
    notification_type=TimedNotificationType.WHATSAPP,
    content="Meeting reminder",
    scheduled_time="2024-01-03T15:00:00Z",
    recipient_timezone="Africa/Dar_es_Salaam",
    recipient_phone="1234567890",
    wa=whatsapp_sender.get_json()
)


```

### Features

- Schedule notifications across multiple channels
- Support for various timezones
- Bulk notification creation
- Notification management (update/delete)
- Local time conversion
- Webhook integration for notification events

### Support

If you encounter any problems or have questions:

1. Check the [documentation](https://github.com/Tiririkha/infinity-stones)
2. Open an [issue](https://github.com/Tiririkha/infinity-stones/issues)
3. Submit a [pull request](https://github.com/Tiririkha/infinity-stones/pulls)

### License

[MIT](https://github.com/Tiririkha/infinity-stones/blob/main/LICENSE)