from rest_framework import serializers
from .models import Payment, Transaction, Refund, WebhookEvent, CheckoutSession

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'payment', 'provider_txn_id', 'event', 'status', 'payload', 'created_at']
        read_only_fields = ['id', 'created_at']


class CheckoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutSession
        fields = ['id', 'payment', 'session_id', 'return_url', 'cancel_url', 'expires_at', 'provider_data', 'created_at']
        read_only_fields = ['id', 'session_id', 'provider_data', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'invoice', 'user', 'provider', 'amount', 'currency',
            'status', 'reference', 'provider_payment_id', 'provider_metadata',
            'paid_at', 'created_at', 'updated_at', 'transactions'
        ]
        read_only_fields = ['id', 'status', 'paid_at', 'created_at', 'updated_at', 'provider_payment_id', 'provider_metadata', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and not validated_data.get('user'):
            validated_data['user'] = request.user
        return super().create(validated_data)


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'amount', 'reason', 'status', 'provider_refund_id', 'created_at', 'processed_at', 'metadata']
        read_only_fields = ['id', 'status', 'provider_refund_id', 'created_at', 'processed_at']


class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = ['id', 'provider', 'event_type', 'signature', 'payload', 'processed', 'created_at', 'processed_at', 'note']
        read_only_fields = ['id', 'processed', 'created_at', 'processed_at']
