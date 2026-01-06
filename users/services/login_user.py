from users.models import CustomUser 
from core.exceptions.error_messages import ErrorCodes
from django.contrib.auth.hashers import  check_password
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions.exception import CustomApiException








def login_user(data):
    email = data.get("email")
    password = data.get("password")
    user = CustomUser.objects.filter(email=email, is_verified=True).first()
    if not user:
        raise CustomApiException(ErrorCodes.NOT_FOUND,message="Foydalanuvchi topilmadi")
    elif not user.is_verified:
        raise CustomApiException(ErrorCodes.NOT_VERIFIED,message="Foydalanuvchi tasdiqlanmagan.")
    if not check_password(password, user.password):
        raise CustomApiException(ErrorCodes.INVALID_INPUT,message="Noto'g'ri parol.")
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }
    