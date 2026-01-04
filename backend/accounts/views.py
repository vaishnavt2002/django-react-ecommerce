from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import RegisterSerializer, VerifyOTPSerializer
from accounts.services.registration_flow_service import RegistrationFlowService


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
