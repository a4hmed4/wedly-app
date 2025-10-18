from django.contrib import admin
from .models import Booking, ServiceBooking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'venue', 'event_date', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'event_date')
    search_fields = ('user__username', 'venue__name')


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('booking', 'service', 'quantity', 'price')
