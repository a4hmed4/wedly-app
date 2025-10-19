# payments/utils.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from decimal import Decimal

def egp(amount):
    return f"{Decimal(amount):.2f} EGP"


def generate_payment_receipt_pdf(payment):
    """
    Returns bytes of PDF receipt for a Payment instance.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, height - 80, "Payment Receipt")

    p.setFont("Helvetica", 11)
    p.drawString(40, height - 110, f"Receipt ID: PAY-{payment.id}")
    p.drawString(40, height - 130, f"Date: {payment.paid_at or payment.created_at}")
    p.drawString(40, height - 150, f"Payer: {payment.user.username} ({payment.user.email})")
    p.drawString(40, height - 170, f"Booking: {getattr(payment.booking, 'id', '')}")
    p.drawString(40, height - 190, f"Amount: {payment.amount} {payment.currency}")
    p.drawString(40, height - 210, f"Provider: {payment.get_provider_display()}")

    p.line(40, height - 220, width - 40, height - 220)

    # Footer / notes
    p.setFont("Helvetica-Oblique", 9)
    p.drawString(40, 40, "Thank you for using WedlyApp.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.read()


def send_payment_receipt_email(payment):
    """
    Generate PDF and send to payer (and optionally owner).
    """
    subject = f"Payment Receipt - {payment.booking} - #{payment.id}"
    message = f"Dear {payment.user.username},\n\nAttached is your payment receipt.\n\nThank you."
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [payment.user.email])
    pdf_bytes = generate_payment_receipt_pdf(payment)
    email.attach(f"receipt_{payment.id}.pdf", pdf_bytes, 'application/pdf')
    email.send(fail_silently=True)

    # also send to venue owner
    try:
        owner_email = payment.booking.hall.venue.owner.email
        if owner_email:
            email_owner = EmailMessage(f"Payment Received - Booking #{payment.booking.id}",
                                      f"Payment of {payment.amount} was received for booking #{payment.booking.id}.",
                                      settings.DEFAULT_FROM_EMAIL, [owner_email])
            email_owner.attach(f"receipt_{payment.id}.pdf", pdf_bytes, 'application/pdf')
            email_owner.send(fail_silently=True)
    except Exception:
        pass
