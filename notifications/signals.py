from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from bookings.models import Booking
from .models import Notification
from .utils import send_notification_email


@receiver(post_save, sender=Booking)
def booking_notifications(sender, instance, created, **kwargs):
    if created:
        msg_user = f"تم استلام طلب حجزك في {instance.hall.name} بتاريخ {instance.date}."
        Notification.objects.create(
            recipient=instance.user,
            event_type='BOOKING_CREATED',
            message=msg_user
        )
        send_notification_email(instance.user, "📅 تم استلام حجزك بنجاح", msg_user)

        msg_owner = f"قام {instance.user.username} بحجز {instance.hall.name} بتاريخ {instance.date}."
        Notification.objects.create(
            recipient=instance.hall.venue.owner,
            event_type='BOOKING_CREATED',
            message=msg_owner
        )
        send_notification_email(instance.hall.venue.owner, "🛎️ تم استلام حجز جديد", msg_owner)

    else:
        try:
            old = Booking.objects.get(pk=instance.pk)
        except Booking.DoesNotExist:
            old = None

        if old:
            changed_fields = []
            if old.date != instance.date:
                changed_fields.append("تاريخ الحجز")
            if old.total_guests != instance.total_guests:
                changed_fields.append("عدد الضيوف")

            if changed_fields:
                changes = " و ".join(changed_fields)
                msg_user = f"تم تعديل {changes} في حجزك بـ {instance.hall.name}."
                msg_owner = f"قام {instance.user.username} بتعديل {changes} في الحجز الخاص به بـ {instance.hall.name}."

                Notification.objects.bulk_create([
                    Notification(recipient=instance.user, event_type='BOOKING_UPDATED', message=msg_user),
                    Notification(recipient=instance.hall.venue.owner, event_type='BOOKING_UPDATED', message=msg_owner)
                ])

                send_notification_email(instance.user, "🔄 تم تعديل تفاصيل الحجز", msg_user)
                send_notification_email(instance.hall.venue.owner, "✏️ تم تعديل حجز أحد العملاء", msg_owner)

    if instance.status == "CONFIRMED":
        msg_user = f"تم تأكيد حجزك لـ {instance.hall.name} بنجاح 🎉"
        Notification.objects.create(
            recipient=instance.user,
            event_type='BOOKING_CONFIRMED',
            message=msg_user
        )
        send_notification_email(instance.user, "✅ تم تأكيد الحجز", msg_user)

    elif instance.status == "CANCELLED":
        msg_user = f"تم إلغاء حجزك لـ {instance.hall.name}."
        msg_owner = f"قام {instance.user.username} بإلغاء الحجز لـ {instance.hall.name}."

        Notification.objects.bulk_create([
            Notification(recipient=instance.user, event_type='BOOKING_CANCELLED', message=msg_user),
            Notification(recipient=instance.hall.venue.owner, event_type='BOOKING_CANCELLED', message=msg_owner)
        ])

        send_notification_email(instance.user, "❌ تم إلغاء الحجز", msg_user)
        send_notification_email(instance.hall.venue.owner, "⚠️ تم إلغاء حجز", msg_owner)


@receiver(post_save, sender=Booking)
def booking_review_notification(sender, instance, **kwargs):
    if instance.rating and instance.status == "COMPLETED":
        msg_owner = f"قام {instance.user.username} بتقييم خدمتك في {instance.hall.name} بـ {instance.rating} نجوم."
        Notification.objects.create(
            recipient=instance.hall.venue.owner,
            event_type='BOOKING_RATED',
            message=msg_owner
        )
        send_notification_email(instance.hall.venue.owner, "⭐ تقييم جديد من عميل", msg_owner)
