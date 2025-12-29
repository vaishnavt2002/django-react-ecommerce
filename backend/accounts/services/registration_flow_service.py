from accounts.services.otp_service import OTPService
from accounts.services.temp_registration_service import TempRegistrationSerive

class RegistrationFlowService:
    def __init__(self):
        self.otp_service = OTPService()
        self.temp_service = TempRegistrationSerive()

    def start(self, *, email: str, password: str) -> dict:
        verification_id = self.temp_service.create(email=email, password=password)
        otp, otp_hash = self.otp_service.generate()
        self.temp_service.set_otp(verification_id=verification_id, otp_hash=otp_hash)
        return {"verification_id": verification_id, "otp": otp}
    
    def verify(self, *, verification_id: str, otp: str) -> bool:
        data = self.temp_service.get(verification_id)
        if not data:
            raise ValueError("Invalid or expired verification session")
        
        if not self.otp_service.verify(raw_otp=otp, hashed_otp= data['otp_hash']):
            self.temp_service.increment_attempts(verification_id)
            raise ValueError("Invalid OTP")
        
        self.temp_service.delete(verification_id)
        return data
