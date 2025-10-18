from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Venue, Hall, Booking
from datetime import date, time

User = get_user_model()


class BookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass')
        self.venue = Venue.objects.create(owner=self.user, name='Venue 1')
        self.hall = Hall.objects.create(
            venue=self.venue,
            name='Main Hall',
            capacity=100,
            pricing_type=Hall.PricingType.PER_DAY,
            price_per_day=1000
        )

    def test_full_day_overlap(self):
        Booking.objects.create(
            user=self.user,
            hall=self.hall,
            date=date(2030, 1, 1),
            total_price=1000
        )
        with self.assertRaises(Exception):
            b = Booking(
                user=self.user,
                hall=self.hall,
                date=date(2030, 1, 1),
                total_price=1000
            )
            b.clean()

    def test_time_slot_overlap(self):
        self.hall.pricing_type = Hall.PricingType.PER_HOUR
        self.hall.price_per_hour = 100
        self.hall.save()

        Booking.objects.create(
            user=self.user,
            hall=self.hall,
            date=date(2030, 2, 1),
            start_time=time(10, 0),
            end_time=time(12, 0),
            total_price=200
        )

        with self.assertRaises(Exception):
            b = Booking(
                user=self.user,
                hall=self.hall,
                date=date(2030, 2, 1),
                start_time=time(11, 0),
                end_time=time(13, 0),
                total_price=200
            )
            b.clean()
