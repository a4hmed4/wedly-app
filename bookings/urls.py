from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, CreateOrUpdateBookingView


router = DefaultRouter()
router.register('book', BookingViewSet, basename='booking')


urlpatterns = [
    path('', include(router.urls)),
    # Expose create/update booking as a dedicated POST endpoint using ViewSet action mapping
    path('bookings/', CreateOrUpdateBookingView.as_view({'post': 'post'}), name='booking-create-update'),
]
