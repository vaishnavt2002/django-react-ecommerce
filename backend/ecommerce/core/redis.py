from django.conf import settings
from django_redis import get_redis_connection

def get_auth_redis():
    return get_redis_connection("auth")