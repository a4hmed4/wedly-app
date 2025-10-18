from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    VerifyEmailView,
    OwnerDashboardView,
    ServiceProviderDashboardView,
    UserDashboardView,
    PasswordResetRequestView,
    UploadProfileImageView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('upload-profile-image/', UploadProfileImageView.as_view(), name='upload-profile-image'),
    # Dashboards
    path('dashboard/owner/', OwnerDashboardView.as_view(), name='owner-dashboard'),
    path('dashboard/service/', ServiceProviderDashboardView.as_view(), name='service-dashboard'),
    path('dashboard/user/', UserDashboardView.as_view(), name='user-dashboard'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset'),


]
