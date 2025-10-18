from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentViewSet, RefundViewSet, TransactionViewSet,
    WebhookReceiverView, CheckoutSessionViewSet
)

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payment')
router.register('refunds', RefundViewSet, basename='refund')
router.register('transactions', TransactionViewSet, basename='transaction')
router.register('checkout-sessions', CheckoutSessionViewSet, basename='checkout-session')

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/<str:provider>/', WebhookReceiverView.as_view(), name='payments-webhook'),
]
