from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import RegisterSerializer, VerifyOTPSerializer, LoginSerializer
from accounts.services.registration_flow_service import RegistrationFlowService
from accounts.services.auth_service import AuthService
from accounts.services.token_service import TokenService
from ecommerce.core.logging import get_logger
import uuid

logger = get_logger(__name__)

class RegisterAPIView(APIView):
    def post(self, request):

        logger.info(
            "registration_api_called",
        )

        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "registration_validation_failed",
                errors=serializer.errors
            )
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            service = RegistrationFlowService()
            result = service.start(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"]
            )
            
            logger.info(
                "registration_api_success",
                verification_id=result.get('verification_id')
            )
            
            return Response(result, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            logger.warning(
                "registration_api_business_error",
                error=str(e)
            )
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                "registration_api_system_error",
                error=str(e),
                exc_info=True
            )
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class VerifyOTPAPIView(APIView):
    def post(self, request):
        logger.info("otp_verification_api_called")

        serializer = VerifyOTPSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning(
                "otp_verification_validation_failed",
                errors=serializer.errors
            )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


        try:
            service = RegistrationFlowService()
            service.verify(
                verification_id=serializer.validated_data["verification_id"],
                otp=serializer.validated_data["otp"]
            )

            logger.info("otp_verification_api_success")
            
            return Response(
                {"message": "Registration verified successfully"},
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            logger.warning(
                "otp_verification_api_business_error",
                error=str(e)
            )
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(
                "otp_verification_api_system_error",
                error=str(e),
                exc_info=True
            )
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginAPIView(APIView):
    def post(self, request):

        logger.info(
            "login_api_called",
        )

        serializer = LoginSerializer(data = request.data)

        if not serializer.is_valid():
            logger.warning(
                "login_validation_failed",
                errors=serializer.errors
            )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        service = AuthService()

        try:
            service = AuthService()
            result = service.login(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            response = Response(
                {"message": "Login successful"},
                status=status.HTTP_200_OK
            )
            
            # Set secure cookies
            response.set_cookie(
                key="access_token",
                value=result["access_token"],
                httponly=True,
                secure=True, 
                samesite="Strict",
                max_age=15 * 60
            )
            
            response.set_cookie(
                key="refresh_token",
                value=result["refresh_token"],
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=7 * 24 * 60 * 60
            )
            
            logger.info(
                "login_api_success",
                user_id=result['user'].id
            )
            
            return response
            
        except ValueError as e:
            logger.warning(
                "login_api_failed",
                error=str(e)
            )
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.error(
                "login_api_system_error",
                error=str(e),
                exc_info=True
            )
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

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
            value=tokens["access_token"],
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=1 * 60
        )

        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=7 * 24 * 60 * 60
        )

        return response
            