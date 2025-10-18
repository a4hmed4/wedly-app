# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import User
from services.models import Service
from halls.models import Venue
from bookings.models import Booking

User = get_user_model()


# ========================  Register Serializer ========================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    phone = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=User.Gender.choices)
    role = serializers.ChoiceField(choices=User.Role.choices)
    business_type = serializers.ChoiceField(
        choices=User.BusinessType.choices,
        required=False,
        default=User.BusinessType.NONE,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone",
            "gender",
            "password",
            "confirm_password",
            "role",
            "business_type",
        ]

    def validate(self, data):
        """تأكيد صحة البيانات"""
        # تأكيد تطابق كلمة المرور
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")

        # لو المستخدم Service Provider لازم يحدد نوع الخدمة
        if (
            data["role"] == User.Role.SERVICE
            and data.get("business_type") == User.BusinessType.NONE
        ):
            raise serializers.ValidationError(
                {
                    "business_type": "Service providers must select a valid business type."
                }
            )

        return data

    def create(self, validated_data):
        from services.models import Service
        from halls.models import Venue

        validated_data.pop("confirm_password")

        # تعيين business_type تلقائيًا حسب الدور إذا لم يُحدد
        role = validated_data.get("role", User.Role.USER)
        if role == User.Role.OWNER:
            validated_data["business_type"] = User.BusinessType.HALL
        elif role == User.Role.SERVICE and validated_data.get("business_type") in [
            None,
            User.BusinessType.NONE,
        ]:
            validated_data["business_type"] = (
                User.BusinessType.MAKEUP
            )  # أو أي default مناسبة
        else:
            validated_data["business_type"] = User.BusinessType.NONE

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            gender=validated_data["gender"],
            password=validated_data["password"],
            role=role,
            business_type=validated_data["business_type"],
        )
        user.is_active = False
        user.save()

        # إنشاء Service / Venue تلقائيًا
        if user.role == User.Role.SERVICE:
            Service.objects.create(
                provider=user,
                name=f"{user.username}'s {user.get_business_type_display()}",
                service_type=user.business_type,
                description="Add your service details here.",
                price = 0.00,
            )
        elif user.role == User.Role.OWNER:
            Venue.objects.create(
                owner=user,
                name=f"{user.username}'s Venue",
                description="Add your venue description here.",
                address="Not specified",
            )

        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        """إرسال رابط تحقق من الإيميل"""
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        verify_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"

        subject = "🔐 Verify your Wedly account"
        message = (
            f"Hello {user.username},\n\n"
            f"Please cofirm that you created account as a {user.Role}, \n\n"
            f"Please verify your email to activate your account:\n"
            f"{verify_link}\n\n"
            f"Thank you for joining Wedly app 💍"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


# ========================  User Serializer ========================
class UserSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    venues = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "business_type",
                  "stats", "venues", "services", "bookings"]

    def get_stats(self, obj):
        if obj.role == User.Role.OWNER:
            return {
                "total_venues": obj.venues.count(),
                "total_bookings": Booking.objects.filter(venue__owner=obj).count(),
            }
        elif obj.role == User.Role.SERVICE:
            return {
                "total_services": obj.services.count(),
                "total_bookings": Booking.objects.filter(service__provider=obj).count(),
            }
        elif obj.role == User.Role.USER:
            return {"total_bookings": obj.bookings.count()}
        return {}

    def get_venues(self, obj):
        if obj.role == User.Role.OWNER:
            return [
                {"id": v.id, "name": v.name, "address": v.address, "capacity": v.capacity, "price": v.price_per_day}
                for v in obj.venues.all()
            ]
        return []

    def get_services(self, obj):
        if obj.role == User.Role.SERVICE:
            return [
                {"id": s.id, "name": s.name, "category": s.get_service_type_display(), "price": s.price}
                for s in obj.services.all()
            ]
        return []

    def get_bookings(self, obj):
        if obj.role == User.Role.USER:
            return [
                {"id": b.id, "venue": b.venue.name, "status": b.status, "date": b.event_date, "total_price": b.total_price}
                for b in obj.bookings.all()
            ]
        return []


# ========================  Dashboard Serializer ========================
class UserDashboardSerializer(serializers.ModelSerializer):
    """ملف المستخدم الكامل لعرضه في الـ Dashboard"""

    stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "business_type", "stats"]

    def get_stats(self, obj):
        """إحصائيات سريعة لكل نوع مستخدم"""
        if obj.role == User.Role.OWNER:
            return {
                "total_venues": obj.venues.count(),
                "total_bookings": Booking.objects.filter(venue__owner=obj).count(),
            }
        elif obj.role == User.Role.SERVICE:
            return {
                "total_services": obj.services.count(),
                "total_bookings": Booking.objects.filter(service__provider=obj).count(),
            }
        elif obj.role == User.Role.USER:
            return {"total_bookings": obj.bookings.count()}
        return {}


# ======================== Reset Pass ========================


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            # لا تفصح إن الايميل غير موجود — لكن يمكنك رفع خطأ لو حابب
            pass
        return value

    def save(self):
        email = self.validated_data["email"]
        users = User.objects.filter(email__iexact=email)
        for user in users:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = (
                f"{settings.FRONTEND_URL}/reset-password-confirm/{uid}/{token}/"
            )
            subject = "Reset your WeddingApp password"
            message = f"Hi {user.username},\n\nClick the link to reset your password:\n{reset_link}\n\nIf you didn't request this, ignore."
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']