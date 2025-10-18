from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# ====================== Venue ======================
class Venue(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='venues')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ====================== Hall ======================
class Hall(models.Model):
    class PricingType(models.TextChoices):
        PER_HOUR = 'PER_HOUR', 'Per Hour'
        PER_DAY = 'PER_DAY', 'Per Day'

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='halls')
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=100)
    pricing_type = models.CharField(max_length=10, choices=PricingType.choices)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    reviews_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_featured = models.BooleanField(default=False, help_text="Show as featured on homepage")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Percentage discount (0-100)")

    def get_price_after_discount(self):
       
        if self.discount_percent and self.discount_percent > 0:
            if self.pricing_type == self.PricingType.PER_DAY and self.price_per_day:
                return (self.price_per_day * (100 - self.discount_percent)) / 100
            if self.pricing_type == self.PricingType.PER_HOUR and self.price_per_hour:
                return (self.price_per_hour * (100 - self.discount_percent)) / 100
        # no discount
        return self.price_per_day if self.pricing_type == self.PricingType.PER_DAY else self.price_per_hour

    

    def __str__(self):
        return f"{self.name} ({self.venue.name})"


# ====================== Hall Images ======================
class HallImage(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='halls/images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.hall.name} - Image {self.id}"


# ====================== Catering Options ======================
class CateringOption(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='catering_options')
    name = models.CharField(max_length=100)
    price_per_person = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.hall.name}"


# ====================== Amenities ======================
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

