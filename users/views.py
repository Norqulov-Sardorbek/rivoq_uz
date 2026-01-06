from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from users.services.login_user import login_user
from users.services.verify_user import verify_otp
from core.exceptions.error_messages import ErrorCodes
from users.services.otp_user import send_otp_via_email
from core.exceptions.exception import CustomApiException
from users.services.get_user_profile import get_user_profile
from users.services.change_password_user import verify_user, change_password


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class RegisterView(APIView):

    @swagger_auto_schema(
        operation_description="Register a new user",
        operation_summary="User Registration",
        request_body=EmailSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response("OTP sent successfully."),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid input.")
        }
    )
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
              raise CustomApiException(ErrorCodes.INVALID_INPUT, message="Noto'g'ri ma'lumot kiritildi.")

        
        
        if not send_otp_via_email(serializer.validated_data):
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message="Email yuborishda xatolik yuz berdi.")

        return Response({"message": "OTP muvaffaqiyatli yuborildi"}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    @swagger_auto_schema(
        operation_description="Verify OTP and register the user",
        operation_summary="Verify OTP",
        request_body=VerifyOTPSerializer,
        responses={
            status.HTTP_200_OK: TokenSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid input or OTP."),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found.")
        }
    )

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message="Telefon raqam va OTP talab qilinadi.")

        response=verify_otp(email, otp)
        return Response(response, status=status.HTTP_200_OK)
    
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login user and obtain JWT tokens",
        operation_summary="User Login",
        request_body=EmailSerializer,
        responses={
            status.HTTP_200_OK: TokenSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid input."),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found.")
        }
    )

    def post(self, request):
        email = request.data.get('email')

        if not email:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message="Email talab qilinadi.")

        response=login_user({
            "email": email
        })
        return Response(response, status=status.HTTP_200_OK)
        
class UserProfileAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the profile of the authenticated user",
        operation_summary="Get User Profile",
        responses={
            status.HTTP_200_OK: UserProfileSerializer,
            status.HTTP_404_NOT_FOUND: openapi.Response("User profile not found.")
        }
    )

    def get(self, request):
        user_id = request.user.id 
        if not user_id:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST, message="Foydalanuvchi topilmadi.")

        profile = get_user_profile(user_id)
        if not profile:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST, message="Foydalanuvchi profili topilmadi.")

        serializer = UserProfileSerializer(profile) 
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    @swagger_auto_schema(
        operation_description="Change the password of the authenticated user",
        operation_summary="Change Password",
        request_body=ChangePasswordSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response("Password changed successfully."),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid input or OTP."),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found.")
        }
    )

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not email or not new_password:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message="Email va yangi parol talab qilinadi.")
        
        change_password({
            "email": email,
            "new_password": new_password
        })

        return Response({"message": "Parol muvaffaqiyatli o'zgartirildi."}, status=status.HTTP_200_OK)
    
class VerifyOrSendOtpUserView(APIView):
    @swagger_auto_schema(
        operation_description="Parol ozgartish vaqtida foydalanuvchini tasdiqlash yoki OTP yuborish. Emailni ozi jonatilda emailga otp jonatadi agar qoshib otp ham yuborilsa uni tasdiqlaydi",
        operation_summary="Verify User",
        request_body=VerifyOTPSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response("User verified successfully."),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid input or OTP."),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found.")
        }
    )

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message="Email talab qilinadi.")

        response=verify_user({
            "email": email,
            "otp": otp
        })
        return Response(response, status=status.HTTP_200_OK)