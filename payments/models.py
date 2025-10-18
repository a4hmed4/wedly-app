from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCEEDED = 'SUCCEEDED', 'Succeeded'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    class Provider(models.TextChoices):
        CASH = 'cash', 'Cash'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
        VODAFONE_CASH = 'vodafone_cash', 'Vodafone Cash'
        INSTAPAY = 'instapay', 'Instapay'
        PAYPAL = 'paypal', 'PayPal'
        STRIPE = 'stripe', 'Stripe'  

    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments')
    invoice = models.ForeignKey('bookings.Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    # بيانات الدفع
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=30, choices=Provider.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='EGP')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reference = models.CharField(max_length=100, blank=True, help_text='Local reference (order id)')
    provider_payment_id = models.CharField(max_length=100, blank=True, help_text='Gateway payment id')
    provider_metadata = models.JSONField(default=dict, blank=True)

    # تواريخ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} | {self.amount} {self.currency} | {self.get_status_display()}"


class Transaction(models.Model):
    class Event(models.TextChoices):
        INIT = 'INIT', 'Init'
        AUTHORIZE = 'AUTHORIZE', 'Authorize'
        CAPTURE = 'CAPTURE', 'Capture'
        REFUND = 'REFUND', 'Refund'
        WEBHOOK = 'WEBHOOK', 'Webhook'
        FAILURE = 'FAILURE', 'Failure'

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    provider_txn_id = models.CharField(max_length=120, blank=True)
    event = models.CharField(max_length=20, choices=Event.choices)
    status = models.CharField(max_length=20, default='OK')
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Txn {self.event} for Payment #{self.payment_id}"


class Refund(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        PROCESSED = 'PROCESSED', 'Processed'
        FAILED = 'FAILED', 'Failed'

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    provider_refund_id = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Refund #{self.id} for Payment #{self.payment_id}"


class WebhookEvent(models.Model):
    provider = models.CharField(max_length=30)
    event_type = models.CharField(max_length=100, blank=True)
    signature = models.CharField(max_length=255, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Webhook {self.provider} | {self.event_type} | processed={self.processed}"


class CheckoutSession(models.Model):
    """جلسة دفع خارجية (لطرف ثالث)"""
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='checkout_session')
    session_id = models.CharField(max_length=150, unique=True)
    return_url = models.URLField(blank=True)
    cancel_url = models.URLField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    provider_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CheckoutSession #{self.id} for Payment #{self.payment_id}"

class PaymentDistribution(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='distributions')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Distribution to {self.recipient} - {self.amount} EGP"

