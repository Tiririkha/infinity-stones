# Infinity Stones

A Python package providing powerful tools for real-world development challenges.

[![PyPI ](https://badge.fury.io/py/infinitystones.svg)](https://badge.fury.io/py/infinitystones)
[![GitHub](https://img.shields.io/github/license/Tiririkha/infinity-stones)](https://github.com/Tiririkha/infinity-stones/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://github.com/Tiririkha/infinity-stones)

## TimeStone

TimeStone is a notification scheduling and delivery system supporting:

- Email notifications
- Webhook integration
- Custom metadata
- Timezone handling

### Installation

```bash
pip install infinitystones
```

### Quick Start

```python
from infinitystones.timestone.services.notifications import NotificationService
from infinitystones.timestone.models.enums import NotificationType

# Initialize services
notification_service = NotificationService()


def send_welcome_email():
    """Example: Creating and using a template for welcome emails"""

    # 1. Schedule welcome email using the template
    notification = notification_service.create_notification(
        notification_type=NotificationType.EMAIL,
        subject="Welcome to Timestone",
        template="""
            <html>
                <body>
                    <h1>Welcome to Timestone, Eric!</h1>
                    <p>Thank you for joining our platform welcome so much.</p>
                </body>
            </html>
        """,
        recipient_email="maverickweyunga@gmail.com",
        scheduled_time=notification_service.schedule_for(2025, 1, 7, 3, 6),
        recipient_timezone="Africa/Dar_es_Salaam"
    )

    print(f"Scheduled welcome email: {notification.id}")
    return notification


if __name__ == "__main__":
    # Example 1: Send welcome email
    welcome_notification = send_welcome_email()
    print(welcome_notification)

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