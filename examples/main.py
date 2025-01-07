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
