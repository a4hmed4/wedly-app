from django.db import models
from django.conf import settings
from halls.models import Venue
#from services.models import Service

User = settings.AUTH_USER_MODEL


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='bookings')
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')

    def calculate_total(self):
        """جمع سعر القاعة + كل الخدمات"""
        venue_price = self.venue.price
        services_total = sum(service.get_total() for service in self.service_bookings.all())
        self.total_price = venue_price + services_total
        self.save()
        return self.total_price
    def __str__(self):
        return f"Booking #{self.id} - {self.user} ({self.event_date})"

class ServiceBooking(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='service_bookings')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"

#======================= Invoice ========================
class Invoice(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='invoice')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.id} for Booking #{self.booking.id}"
