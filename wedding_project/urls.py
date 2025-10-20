"""
URL configuration for wedding_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Main pages
    path("", views.index_view, name="index"),
    path("admin-access/", views.admin_access_view, name="admin_access"),
    path("api-info/", views.api_info_view, name="api_info"),
    
    # Admin panel
    path("admin/", admin.site.urls),
    # API endpoints (without /api/ prefix)
    path('halls/', include('halls.urls')),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('cloud/', include('cloud.urls')),
    path('notifications/', include('notifications.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),  # oauth endpoint
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
