from ecommerce.core.redis import get_auth_redis
from django.contrib.auth.hashers import make_password
import uuid
from django.utils import timezone
import json
from datetime import timedelta

class TempRegistrationService:
    TTL_SECONDS = 10 * 60
    MAX_ATTEMPTS = 5
    OTP_RESEND_COOLDOWN = timedelta(seconds=60)
    
    def __init__(self):
        self.redis = get_auth_redis()

    def _key(self, verification_id: str) -> str:
        return f"auth:pending:{verification_id}"
    
    def _email_key(self, email: str) -> str:
        return f"auth:pending_email:{email}"
    
    def create_or_refresh(self,*, email:str, raw_password:str) -> str:
        existing_id = self.redis.get(self._email_key(email))

        if existing_id:
            if isinstance(existing_id, bytes):
                existing_id = existing_id.decode("utf-8")
            
            self.refresh(existing_id)
            return existing_id
        verification_id = str(uuid.uuid4())

        payload = {
            "email" : email,
            "password" : raw_password,
            "attempts": 0,
            "created_at": timezone.now().isoformat(),
            "last_otp_sent_at": None
        }
        self.redis.setex(self._key(verification_id), self.TTL_SECONDS, json.dumps(payload))
        self.redis.setex(
            self._email_key(email),
            self.TTL_SECONDS,
            verification_id
        )


        return verification_id
    
    def get(self, verification_id: str) -> dict | None :
        raw = self.redis.get(self._key(verification_id))
        if not raw:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return json.loads(raw)
    
    def increment_attempts(self, verification_id: str):
        data = self.get(verification_id)
        if not data:
            return
        
        data["attempts"] += 1

        if data["attempts"] >= self.MAX_ATTEMPTS:
            self.delete(verification_id)
            return
        self.redis.setex(self._key(verification_id), self.TTL_SECONDS, json.dumps(data))

    def delete(self, verification_id: str):
        data = self.get(verification_id)

        if data:
            self.redis.delete(self._email_key(data["email"]))
        self.redis.delete(self._key(verification_id))

    def set_otp(self, verification_id: str, otp_hash: str):
        data = self.get(verification_id)
        if not data:
            return

        data["otp_hash"] = otp_hash
        data["last_otp_sent_at"] = timezone.now().isoformat()

        self.redis.setex(
            self._key(verification_id),
            self.TTL_SECONDS,
            json.dumps(data)
        )

        
    def refresh(self, verification_id: str):
        data = self.get(verification_id)
        if not data:
            return 
        
        self.redis.setex(self._key(verification_id), self.TTL_SECONDS, json.dumps(data))

    def can_resend_otp(self, data: dict) -> bool:
        last_sent = data.get("last_otp_sent_at")
        if not last_sent:
            return True

        last_sent = timezone.datetime.fromisoformat(last_sent)
        return timezone.now() - last_sent >= self.OTP_RESEND_COOLDOWN


    

    