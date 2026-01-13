from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import RegisterSerializer, VerifyOTPSerializer, LoginSerializer
from accounts.services.registration_flow_service import RegistrationFlowService
from accounts.services.auth_service import AuthService
from accounts.services.token_service import TokenService


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service= RegistrationFlowService()

        result = service.start(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"])
        
        return Response(result, status=status.HTTP_201_CREATED)
    
class VerifyOTPAPIView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = RegistrationFlowService()

        try:
            service.verify(
                verification_id=serializer.validated_data["verification_id"],
                otp=serializer.validated_data["otp"]
            )
        except ValueError as e:
            return Response(
                {"error":str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
                {"message":"Registartion verified successsfully"},
                status=status.HTTP_200_OK
            )
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthService()

        try:
            result = service.login(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
        except ValueError as e:
            return Response({'error': str(e)}, status= status.HTTP_400_BAD_REQUEST)
        
        response = Response(
                {"message":"Login Successfull"},
                status=status.HTTP_200_OK
            )
        
        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=15*60
        )

        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60
        )
        return response

class RefreshTokenAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error":"Refresh token is not provided"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        service = TokenService()

        try:
            tokens = service.refresh_access_token(refresh_token=refresh_token)
        except ValueError as e:
            return Response(
                {"error":str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        response = Response(
            {"message":"Token refreshed"},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=1 * 60
        )

        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60
        )

        return response
            