from rest_framework import serializers
from .models import Booking, ServiceBooking
from services.serializers import ServiceSerializer
from halls.serializers import VenueSerializer


class ServiceBookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = ServiceBooking
        fields = ['id', 'service', 'quantity', 'price']


class BookingSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    service_bookings = ServiceBookingSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'venue', 'event_date', 'total_price', 'status', 'service_bookings', 'created_at']
        read_only_fields = ['user', 'total_price', 'status', 'created_at']
