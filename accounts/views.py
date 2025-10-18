from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from .models import User
from .serializers import RegisterSerializer, UserSerializer, PasswordResetRequestSerializer, ProfileImageSerializer

# Import related serializers for dashboards
from halls.models import Venue
from halls.serializers import VenueSerializer
from services.models import ExtraService
from services.serializers import ExtraServiceSerializer
from bookings.models import Booking
from bookings.serializers import BookingSerializer

from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime



User = get_user_model()


# ============================================================
#  AUTHENTICATION VIEWS
# ============================================================

class RegisterView(generics.CreateAPIView):
    """Register new user"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """
    Login View — returns access & refresh tokens for the user.
    JWT authentication handled automatically by SimpleJWT.
    """
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    """Return the authenticated user's profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response({"error": "❌ Token is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            exp_timestamp = access_token["exp"]
            exp_time = datetime.fromtimestamp(exp_timestamp)

            if exp_time < datetime.now():
                return Response({"error": "❌ Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=user_id)
            if user.is_active:
                return Response({"message": "✅ Email already verified."}, status=status.HTTP_200_OK)

            user.is_active = True
            user.save()
            return Response({"message": "✅ Email verified successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"❌ Invalid or expired token. ({str(e)})"}, status=status.HTTP_400_BAD_REQUEST)



class UploadProfileImageView(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ============================================================
#  DASHBOARD VIEWS (Role-Based)
# ============================================================

class OwnerDashboardView(APIView):
    """Dashboard for Venue Owners — show owned venues"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != User.Role.OWNER:
            return Response({'error': 'Access denied. Not an owner account.'}, status=status.HTTP_403_FORBIDDEN)

        venues = Venue.objects.filter(owner=user)
        venues_data = VenueSerializer(venues, many=True).data
        user_data = UserSerializer(user).data
        user_data["owned_venues"] = venues_data

        return Response(user_data, status=status.HTTP_200_OK)


class ServiceProviderDashboardView(APIView):
    """Dashboard for Service Providers — show provided services"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != User.Role.SERVICE:
            return Response({'error': 'Access denied. Not a service provider.'}, status=status.HTTP_403_FORBIDDEN)

        services = ExtraService.objects.filter(provider=user)
        services_data = ExtraServiceSerializer(services, many=True).data
        user_data = UserSerializer(user).data
        user_data["provided_services"] = services_data

        return Response(user_data, status=status.HTTP_200_OK)


class UserDashboardView(APIView):
    """Dashboard for Customers — show bookings"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != User.Role.USER:
            return Response({'error': 'Access denied. Not a regular user.'}, status=status.HTTP_403_FORBIDDEN)

        bookings = Booking.objects.filter(user=user)
        bookings_data = BookingSerializer(bookings, many=True).data
        user_data = UserSerializer(user).data
        user_data["bookings"] = bookings_data

        return Response(user_data, status=status.HTTP_200_OK)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'detail': 'If the email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)