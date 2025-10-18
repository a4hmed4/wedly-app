# payments/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, PaymentDistribution
from bookings.models import Booking

@receiver(post_save, sender=Payment)
def handle_payment_success(sender, instance, created, **kwargs):
    if not created and instance.status == Payment.Status.SUCCEEDED:
        booking = instance.booking
        venue_owner = booking.venue.owner

        # توزيع القاعة
        PaymentDistribution.objects.create(
            payment=instance,
            recipient=venue_owner,
            amount=booking.venue.price,
            note="Venue payment"
        )

        # توزيع الخدمات
        for sb in booking.service_bookings.all():
            PaymentDistribution.objects.create(
                payment=instance,
                recipient=sb.service.provider,
                amount=sb.get_total(),
                note=f"Payment for service: {sb.service.name}"
            )
