from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueViewSet, HallViewSet, AmenityViewSet, CateringOptionViewSet

router = DefaultRouter()
router.register('venues', VenueViewSet, basename='venue')
router.register('halls', HallViewSet, basename='hall')
router.register('halls/featured', HallViewSet, basename='hall_featured')
router.register('amenities', AmenityViewSet, basename='amenity')
router.register('catering-options', CateringOptionViewSet, basename='catering-option')

urlpatterns = [
    path('', include(router.urls)),
]
