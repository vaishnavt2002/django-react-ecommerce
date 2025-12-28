import random
from django.contrib.auth.hashers import check_password, make_password

class OTPService:
    OTP_LENGTH = 6

    def generate(self) -> tuple[str,str]:
        otp = "".join(str(random.randint(0,9)) for _ in range(self.OTP_LENGTH))
        return otp, make_password(otp)
    
    def verify(self, *, raw_otp: str, hashed_otp: str) -> bool:
        return check_password(raw_otp, hashed_otp)
    
    