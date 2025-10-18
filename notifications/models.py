from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    EVENT_TYPES = [
    ('BOOKING_CREATED', 'Booking Created'),
    ('BOOKING_UPDATED', 'Booking Updated'),
    ('BOOKING_CONFIRMED', 'Booking Confirmed'),
    ('BOOKING_CANCELLED', 'Booking Cancelled'),
    ('BOOKING_RATED', 'Booking Rated'),
]


    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} → {self.recipient.username}"
