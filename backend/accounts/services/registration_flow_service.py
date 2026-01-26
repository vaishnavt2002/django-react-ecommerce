from accounts.services.otp_service import OTPService
from accounts.services.temp_registration_service import TempRegistrationService
from accounts.services.notification_service import NotificationService
from accounts.services.user_service import UserService
from ecommerce.core.logging import get_logger

logger = get_logger(__name__)

class RegistrationFlowService:
    def __init__(
            self,
            otp_service: OTPService = None,
            temp_service: TempRegistrationService = None,
            notification_service: NotificationService = None,
            user_service: UserService = None
    ):
        self.otp_service = otp_service or OTPService()
        self.temp_service = temp_service or TempRegistrationService()
        self.notification_service = notification_service or NotificationService()
        self.user_service = user_service or UserService()

    def start(self, *, email: str, password: str) -> dict:
        logger.info(
            "registration_started",
            email_domain=email.split('@')[1]
        )
        try:
            if self.user_service.user_exist(email=email):
                logger.warning(
                    "registration_blocked_duplicate_email",
                    email_domain=email.split('@')[1]
                )
                raise ValueError("User already registered")
            
            verification_id = self.temp_service.create_or_refresh(email=email, raw_password=password)

            data = self.temp_service.get(verification_id)
            if not data:
                logger.error(
                    "registration_session_lost",
                    verification_id=verification_id
                )
                raise ValueError("Registration session expired")
            
            if not self.temp_service.can_resend_otp(data):
                logger.info(
                    "otp_resend_rate_limited",
                    verification_id=verification_id,
                    email_domain=email.split('@')[1]
                )
                return {"verification_id": verification_id}
            otp, otp_hash = self.otp_service.generate()
            self.temp_service.set_otp(verification_id=verification_id, otp_hash=otp_hash)

            logger.info(
                "otp_generated",
                verification_id=verification_id,
                email_domain=email.split('@')[1]
            )


            self.notification_service.send_otp_email(email=email, otp=otp)

            logger.info(
                "otp_email_dispatched",
                verification_id=verification_id,
                email_domain=email.split('@')[1]
            )

            logger.info(
                "registration_flow_completed",
                verification_id=verification_id,
            )
            return {"verification_id": verification_id}
        
        except ValueError as e:
            logger.warning(
                "registration_validation_failed",
                error=str(e),
                email_domain=email.split('@')[1]
            )
            raise
        except Exception as e:
            logger.error(
                "registration_flow_failed",
                error=str(e),
                email_domain=email.split('@')[1],
                exc_info=True
            )
            raise
    
    def verify(self, *, verification_id: str, otp: str) -> bool:
        logger.info(
            "otp_verification_started",
            verification_id=verification_id
        )
        try:
            data = self.temp_service.get(verification_id)
            if not data:
                logger.warning(
                    "otp_verification_invalid_session",
                    verification_id=verification_id
                )
                raise ValueError("Invalid or expired verification session")
            
            attempts = data.get('attempts', 0)
            logger.info(
                "otp_verification_attempt",
                verification_id=verification_id,
                attempt_number=attempts + 1,
                max_attempts=self.temp_service.MAX_ATTEMPTS
            )
            
            if not self.otp_service.verify(raw_otp=otp, hashed_otp= data['otp_hash']):
                self.temp_service.increment_attempts(verification_id)

                logger.warning(
                    "otp_verification_failed",
                    verification_id=verification_id,
                    attempts=attempts + 1
                )

                raise ValueError("Invalid OTP")
            
            user = self.user_service.create_user_from_verified_data(
                email=data['email'],
                raw_password=data['password']
            )
            
            self.temp_service.delete(verification_id)

            logger.info(
                "registration_completed",
                verification_id=verification_id,
                user_id=user.id,
                email_domain=data['email'].split('@')[1]
            )
            return data
        except ValueError as e:
            logger.warning(
                "otp_verification_error",
                verification_id=verification_id,
                error=str(e)
            )
            raise
        except Exception as e:
            logger.error(
                "otp_verification_system_error",
                verification_id=verification_id,
                error=str(e),
                exc_info=True
            )
            raise

    def resend_otp():
        pass