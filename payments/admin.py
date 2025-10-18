from django.contrib import admin
from .models import Payment, Transaction, Refund, WebhookEvent, CheckoutSession

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'booking', 'invoice', 'provider', 'amount', 'currency', 'status', 'paid_at', 'created_at')
    list_filter = ('status', 'provider', 'currency')
    search_fields = ('id', 'reference', 'provider_payment_id', 'user__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'event', 'status', 'created_at')
    list_filter = ('event', 'status')
    search_fields = ('payment__id', 'provider_txn_id')

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'amount', 'status', 'created_at', 'processed_at')
    list_filter = ('status',)

@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'event_type', 'processed', 'created_at')
    list_filter = ('provider', 'processed')

@admin.register(CheckoutSession)
class CheckoutSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'session_id', 'expires_at', 'created_at')
