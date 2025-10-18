from django.utils import timezone
from .models import CheckoutSession, Transaction

def create_checkout_session_for_provider(payment, return_url=None, cancel_url=None):
    # هنا تربط بمزود الدفع الحقيقي (Instapay / PayPal / Stripe ...)
    session = CheckoutSession.objects.create(
        payment=payment,
        session_id=f'session_{payment.id}_{int(timezone.now().timestamp())}',
        return_url=return_url or '',
        cancel_url=cancel_url or '',
        provider_data={'mock': True, 'provider': payment.provider},
    )
    Transaction.objects.create(payment=payment, event=Transaction.Event.INIT, status='OK', payload={'checkout_session': session.session_id})
    return session

def capture_provider_payment(payment):
    # استبدل بالاتصال الفعلي بـ API المزود
    provider_payment_id = f'prov_{payment.id}'
    provider_metadata = {'captured_at': timezone.now().isoformat()}
    return True, provider_payment_id, provider_metadata

def refund_provider_payment(refund):
    # استبدل بالاتصال الفعلي بـ API المزود
    provider_refund_id = f'ref_{refund.id}'
    meta = {'refunded_at': timezone.now().isoformat()}
    return True, provider_refund_id, meta
