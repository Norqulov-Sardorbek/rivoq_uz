from users.models import  CustomUser 
from users.tasks import send_otp_email_task
from core.exceptions.error_messages import ErrorCodes
from django.contrib.auth.hashers import make_password
from core.exceptions.exception import CustomApiException


def send_otp_via_email(data):
    email = data.get("email")
    password = data.get("password")
    hashed_password = make_password(password)
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        CustomUser.objects.create(email=email, password=hashed_password)
    elif user and user.is_verified:
        raise CustomApiException(ErrorCodes.ALREADY_EXISTS,message="Foydalanuvchi allaqachon mavjud.")
    send_otp_email_task.delay(email)
    return True


