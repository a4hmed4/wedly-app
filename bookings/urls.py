from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, CreateOrUpdateBookingView


router = DefaultRouter()
router.register('book/', BookingViewSet, basename='booking')
router.register('bookings/', CreateOrUpdateBookingView, basename='bookings')


urlpatterns = [
    path('', include(router.urls)),
]
