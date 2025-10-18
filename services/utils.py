# services/utils.py
import uuid
from datetime import datetime

def create_checkout_session_for_provider(provider_id, amount, currency="EGP"):
    """
    Simulate creating a checkout session for a service provider.
    Returns a fake checkout session URL and session ID.
    """
    session_id = str(uuid.uuid4())
    return {
        "session_id": session_id,
        "checkout_url": f"https://fakepaymentgateway.com/session/{session_id}",
        "amount": amount,
        "currency": currency,
        "provider_id": provider_id,
    }

def capture_provider_payment(session_id):
    """
    Simulate capturing a provider payment after successful checkout.
    """
    return {
        "session_id": session_id,
        "status": "captured",
        "timestamp": datetime.utcnow().isoformat(),
    }

def refund_provider_payment(session_id):
    """
    Simulate refunding a payment for a provider booking.
    """
    return {
        "session_id": session_id,
        "status": "refunded",
        "timestamp": datetime.utcnow().isoformat(),
    }
