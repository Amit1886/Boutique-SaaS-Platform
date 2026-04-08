"""
Notification placeholders.

TODO: integrate:
- WhatsApp Business API / Twilio WhatsApp
- Email provider (SendGrid, SES)
- SMS provider (Twilio, Msg91)
"""

from __future__ import annotations


def send_whatsapp_update(phone: str, message: str) -> None:
    # Dummy function: no-op
    return None


def send_email_sms(to: str, message: str) -> None:
    # Dummy function: no-op
    return None

