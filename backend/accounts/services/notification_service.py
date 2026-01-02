from accounts.tasks import send_otp_email_task

class NotificationService:
    def send_otp_email(self, *, email: str, otp: str) -> None:
        send_otp_email_task.delay(email=email, otp=otp)
        
