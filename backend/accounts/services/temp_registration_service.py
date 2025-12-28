from ecommerce.core.redis import get_auth_redis
from django.contrib.auth.hashers import make_password
import uuid
from django.utils import timezone
import json
class TempRegistrationSerive:
    TTL_SECONDS = 10 * 6
    MAX_ATTEMPTS = 5
    
    def __init__(self):
        self.redis = get_auth_redis()

    def _key(self, verification_id: str) -> str:
        return f"auth:pending:{verification_id}"
    
    def create(self,*, email:str, raw_password:str) -> str:
        verification_id = str(uuid.uuid4())

        payload = {
            "email" : email,
            "password" : raw_password,
            "attempts": 0,
            "created_at": timezone.now().isoformat()
        }
        self.redis.setex(self._key(verification_id), self.TTL_SECONDS, json.dumps(payload))

        return verification_id
    
    def get(self, verification_id: str) -> dict | None :
        data = self.redis.get(self._key(verification_id))
        if not data:
            return None
        return json.loads(data)
    
    def increment_attempts(self, verification_id: str):
        data = self.get(verification_id)
        if not data:
            return
        
        data["attempts"] += 1

        if data["attempts"] >= self.MAX_ATTEMPTS:
            self.delete(verification_id)
            return
        self.redis.setex(self._key(verification_id), self.TTL_SECONDS, json.dump(data))

    def delete(self, verification_id: str):
        self.redis.delete(self._key(verification_id))
        
