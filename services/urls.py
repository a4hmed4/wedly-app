from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet,
    ServicePlanViewSet,
    ServicePaymentMethodViewSet,
    ExtraServiceViewSet
)

router = DefaultRouter()
router.register('services', ServiceViewSet, basename='service')
router.register('plans', ServicePlanViewSet, basename='service-plan')
#router.register('bookings', ServiceBookingViewSet, basename='service-booking')
router.register('payments', ServicePaymentMethodViewSet, basename='service-payment')
router.register('extra_services', ExtraServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
