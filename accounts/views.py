from rest_framework import status
from rest_framework import response, status, permissions, views
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import SignupSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer, ResetPasswordSerializer
import random



User = get_user_model() 



class SignupView(views.APIView):
    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            201: openapi.Response("Signup successful", SignupSerializer),
            400: "Bad request - Invalid data",
        },
        operation_summary="User Signup",
        operation_description="Register a new user with first name, last name, email, and password."
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # ✅ Generate tokens

            return Response({
                "message": "Signup successful",
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": str(refresh.access_token),  # ✅ Added access token
                "refresh_token": str(refresh),  # ✅ Added refresh token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response("Login successful", LoginSerializer),
            400: "Bad request - Invalid credentials",
        },
        operation_summary="User Login",
        operation_description="Authenticate user using email and password, and return access tokens."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)  # ✅ Generate tokens

            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "access_token": str(refresh.access_token),  # ✅ Added access token
                "refresh_token": str(refresh),  # ✅ Added refresh token
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            otp_code = random.randint(100000, 999999)  # 6-digit OTP
            OTP.objects.create(user=user, code=otp_code)

            # Send OTP via email
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp_code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            # OTP is valid, return success response
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

