from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs= {"max_retries":3, "countdown": 5})
def send_otp_email_task(self, *, email: str, otp: str):
    send_mail(
        subject="Your OTP for registration",
        message=f"Your OTP is {otp}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False

    )