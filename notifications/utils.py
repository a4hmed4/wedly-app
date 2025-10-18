# notifications/utils.py

from django.core.mail import send_mail
from django.conf import settings
from .models import Notification

def send_notification_email(recipient, title, message, link=None):

    #  إنشاء الإشعار في قاعدة البيانات
    Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        link=link
    )

    # إرسال البريد الإلكتروني
    try:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=False,  # خليه False أثناء التطوير عشان نعرف لو في أخطاء
        )
        print(f"📩 تم إرسال بريد إلكتروني إلى {recipient.email}")
    except Exception as e:
        print(f"❌ فشل إرسال البريد الإلكتروني إلى {recipient.email}: {e}")
