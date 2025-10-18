from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db import transaction as dbtx

from .models import Payment, Transaction, Refund, WebhookEvent, CheckoutSession
from .serializers import (
    PaymentSerializer, RefundSerializer, TransactionSerializer, WebhookEventSerializer, CheckoutSessionSerializer
)
from .permissions import IsOwnerOrStaff
from services.utils import (
    create_checkout_session_for_provider,
    capture_provider_payment,
    refund_provider_payment,
)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        qs = Payment.objects.select_related('booking', 'invoice', 'user')
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, status=Payment.Status.PENDING)
        Transaction.objects.create(payment=payment, event=Transaction.Event.INIT, status='OK', payload={'info': 'created'})

    @action(detail=True, methods=['post'])
    def start_checkout(self, request, pk=None):
        """إنشاء جلسة دفع خارجية"""
        payment = self.get_object()
        session = create_checkout_session_for_provider(payment, return_url=request.data.get('return_url'), cancel_url=request.data.get('cancel_url'))
        ser = CheckoutSessionSerializer(session)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def mark_cash_paid(self, request, pk=None):
        """تأكيد دفع كاش/تحويل بنكي يدويًا (للمالك/الأدمن)"""
        payment = self.get_object()
        if payment.provider not in [Payment.Provider.CASH, Payment.Provider.BANK_TRANSFER, Payment.Provider.VODAFONE_CASH]:
            return Response({'detail': 'Only for offline/manual providers.'}, status=400)

        with dbtx.atomic():
            payment.status = Payment.Status.SUCCEEDED
            payment.paid_at = timezone.now()
            payment.save()
            Transaction.objects.create(payment=payment, event=Transaction.Event.CAPTURE, status='OK', payload={'manual': True})
        return Response(self.get_serializer(payment).data)

    @action(detail=True, methods=['post'])
    def capture(self, request, pk=None):
        """Capture عبر مزود أونلاين (مثال: Instapay/PayPal/Stripe)"""
        payment = self.get_object()
        ok, provider_payment_id, provider_metadata = capture_provider_payment(payment)
        if not ok:
            Transaction.objects.create(payment=payment, event=Transaction.Event.FAILURE, status='ERROR', payload={'action': 'capture'})
            return Response({'detail': 'Capture failed'}, status=400)

        with dbtx.atomic():
            payment.status = Payment.Status.SUCCEEDED
            payment.paid_at = timezone.now()
            payment.provider_payment_id = provider_payment_id or payment.provider_payment_id
            payment.provider_metadata = provider_metadata or payment.provider_metadata
            payment.save()
            Transaction.objects.create(payment=payment, event=Transaction.Event.CAPTURE, status='OK', payload={'provider_payment_id': provider_payment_id})

        return Response(self.get_serializer(payment).data)


class RefundViewSet(viewsets.ModelViewSet):
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        qs = Refund.objects.select_related('payment', 'payment__user')
        if self.request.user.is_staff:
            return qs
        return qs.filter(payment__user=self.request.user)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        refund = self.get_object()
        ok, provider_refund_id, meta = refund_provider_payment(refund)
        if not ok:
            refund.status = Refund.Status.FAILED
            refund.save()
            Transaction.objects.create(payment=refund.payment, event=Transaction.Event.REFUND, status='FAILED', payload={'refund_id': refund.id})
            return Response({'detail': 'Refund failed'}, status=400)

        refund.status = Refund.Status.PROCESSED
        refund.provider_refund_id = provider_refund_id or refund.provider_refund_id
        refund.metadata = meta or refund.metadata
        refund.processed_at = timezone.now()
        refund.save()
        Transaction.objects.create(payment=refund.payment, event=Transaction.Event.REFUND, status='OK', payload={'refund_id': refund.id})
        return Response(self.get_serializer(refund).data)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.select_related('payment', 'payment__user')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CheckoutSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CheckoutSession.objects.select_related('payment', 'payment__user')
    serializer_class = CheckoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]


class WebhookReceiverView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, provider: str):
        # خزّن الحدث أولًا
        event = WebhookEvent.objects.create(
            provider=provider,
            event_type=request.headers.get('X-Event-Type', ''),
            signature=request.headers.get('X-Signature', ''),
            payload=request.data,
            processed=False
        )
        # مثال تبسيطي: توقع وجود payment_id
        payment_id = request.data.get('payment_id')
        status_map = request.data.get('status')

        if not payment_id:
            event.note = 'No payment_id in payload'
            event.save()
            return Response({'detail': 'ignored'}, status=202)

        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            event.note = 'Payment not found'
            event.save()
            return Response({'detail': 'payment not found'}, status=404)

        # عالج الحالة
        with dbtx.atomic():
            if status_map in ['succeeded', 'paid', 'captured']:
                payment.status = Payment.Status.SUCCEEDED
                payment.paid_at = timezone.now()
                Transaction.objects.create(payment=payment, event=Transaction.Event.WEBHOOK, status='OK', payload=request.data)
            elif status_map in ['failed', 'canceled']:
                payment.status = Payment.Status.FAILED
                Transaction.objects.create(payment=payment, event=Transaction.Event.WEBHOOK, status='FAILED', payload=request.data)
            payment.save()
            event.processed = True
            event.processed_at = timezone.now()
            event.save()

        return Response({'detail': 'processed'}, status=200)
