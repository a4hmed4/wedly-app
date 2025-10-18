from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from notifications.models import Notification

@receiver(post_save, sender=Booking)
def send_booking_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Your booking for {instance.venue.name} on {instance.event_date} is pending confirmation."
        )
