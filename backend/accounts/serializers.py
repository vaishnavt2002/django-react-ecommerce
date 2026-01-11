from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)

class VerifyOTPSerializer(serializers.Serializer):
    verification_id = serializers.CharField()
    otp = serializers.CharField(min_length=6, max_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    