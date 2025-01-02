import os
from infinitystones import timestone
from infinitystones.timestone import TimestoneCore, TimedNotificationType
from infinitystones.timestone.timed_notifications import UseWhatsAppTimedNotification
from dotenv import load_dotenv

load_dotenv()

# Initialize Timestone client
client = timestone.TimestoneCore()

whatsapp_sender = UseWhatsAppTimedNotification(
    wa_token=os.getenv("WA_TOKEN"),
    wa_phone_number_id=os.getenv("WA_PHONE_NUMBER_ID"),
)
whatsapp_sender.initialize()

# Create a notification
notification = client.create_timed_notification(
    notification_type=TimedNotificationType.WHATSAPP,
    subject="Whatsapp test chat",
    content="Am notifying this through whatsapp",
    scheduled_time=TimestoneCore.notifyAT(2025, 1, 2, 20, 50),
    wa=whatsapp_sender.get_json(),
    recipient_phone="255747955454",
    webhook_url="https://webhook.site/be95f500-1545-4c38-bc55-fc469578dc8d",
    recipient_email="maverickweyunga@gmail.com",
    recipient_timezone="Africa/Dar_es_Salaam",
)

# Get notification details
notification_details = client.get_timed_notification(notification.id)
print(notification_details)