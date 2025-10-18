from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        OWNER = 'OWNER', 'Venue Owner'
        SERVICE = 'SERVICE', 'Service Provider'
        USER = 'USER', 'Customer'

    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    class BusinessType(models.TextChoices):
        HALL = 'HALL', 'Wedding Hall'
        MAKEUP = 'MAKEUP', 'Makeup Artist'
        ATELIER = 'ATELIER', 'Atelier'
        PHOTOGRAPHY = 'PHOTOGRAPHY', 'Photography & Video'
        SUIT = 'SUIT', 'Suit Rental'
        DECOR = 'DECOR', 'Decoration & Design'
        MUSIC = 'MUSIC', 'Music & Entertainment'
        CARS = 'CARS', 'Wedding Cars'
        CATERING = 'CATERING', 'Catering & Hospitality'
        VIDEO = 'VIDEO', 'Video Production'
        NONE = 'NONE', 'None'

    # === Fields ===
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    business_type = models.CharField(max_length=50, choices=BusinessType.choices, default=BusinessType.NONE)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # === Utility Methods ===
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_absolute_url(self):
        """Redirect user to their dashboard/profile page based on role."""
        if self.role == self.Role.OWNER:
            return reverse('owner-dashboard', kwargs={'pk': self.pk})
        elif self.role == self.Role.SERVICE:
            return reverse('service-dashboard', kwargs={'pk': self.pk})
        elif self.role == self.Role.USER:
            return reverse('user-dashboard', kwargs={'pk': self.pk})
        return reverse('admin:index')

    def is_service_provider(self):
        return self.role == self.Role.SERVICE

    def is_owner(self):
        return self.role == self.Role.OWNER
