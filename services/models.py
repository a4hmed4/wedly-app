from django.db import models
from django.conf import settings
#from bookings.models import ServiceBooking
from decimal import Decimal
from accounts.models import User as AccountsUser

User = settings.AUTH_USER_MODEL


# ============================  Service Categories ============================
SERVICE_TYPE_CHOICES = [
    ('DECORATION', 'Decoration & Design'),
    ('MUSIC', 'Music & Entertainment'),
    ('CARS', 'Wedding Cars'),
    ('PHOTOGRAPHY', 'Photography & Video'),
    ('HOSPITALITY', 'Hospitality & Waiters'),
    ('MAKEUP', 'Makeup Artist'),
    ('DRESS', 'Dress Rental'),
    ('SUIT', 'Suit Rental'),
    ('CATERING', 'Catering Services'),
    ('VIDEO', 'Video Production'),
    ('LIGHTING', 'Lighting & Sound'),
    ('FLOWERS', 'Flowers & Bouquets'),
]


# ============================  Service Model ============================
class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_services')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    business_type = models.CharField(max_length=50, choices=AccountsUser.BusinessType.choices, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.PositiveIntegerField(default=1)
    max_capacity = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['service_type', 'name']

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.name}"


# ============================  Service Plan ============================
class ServicePlan(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.PositiveIntegerField(default=1)
    max_capacity = models.PositiveIntegerField(default=100)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


# ============================ Service Booking ============================
""" class ServiceBooking(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        CONFIRMED = "Confirmed", "Confirmed"
        CANCELED = "Canceled", "Canceled"

    booking = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE, related_name='service_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.quantity) * self.service.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service.name} ({self.get_status_display()})"
 """

# ============================  Payment Method ============================
class ServicePaymentMethod(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('visa', 'Visa'),
        ('instapay', 'Instapay'),
        ('vodafone_cash', 'Vodafone Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='payment_methods')
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    account_name = models.CharField(max_length=150, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service.name} - {self.get_method_display()}"


# ============================  Extra Services ============================
class ExtraService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='extra_services')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['service', 'name']

    def __str__(self):
        return f"{self.name} (Extra for {self.service.name})"
