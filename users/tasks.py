import random
from celery import shared_task
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from users.models import UserOtp

@shared_task(bind=True, retry_backoff=5, retry_kwargs={'max_retries': 3})
def send_otp_email_task(self, email):
    print("✅ CELERY TASK STARTED for:", email)

    otp = str(random.randint(100000, 999999))
    UserOtp.objects.create(email=email, otp_code=otp)

    subject = "Sizning tasdiqlash kodingiz"
    html_message = render_to_string('core/email.html', {'otp': otp})
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        subject,
        plain_message,
        "Rivoq <rivoquz@gmail.com>",
        [email],
    )
    msg.attach_alternative(html_message, "text/html")

    try:
        sent = msg.send(fail_silently=False)
        print("✅ EMAIL SEND RESULT:", sent)
        return sent
    except Exception as e:
        print("❌ EMAIL SEND ERROR:", repr(e))
        raise
