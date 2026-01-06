from users.tasks import send_otp_email_task
from users.models import UserOtp, CustomUser 
from core.exceptions.error_messages import ErrorCodes
from django.contrib.auth.hashers import make_password
from core.exceptions.exception import CustomApiException


def verify_user(data):
    email = data.get("email")
    otp = data.get("otp")
    user= CustomUser.objects.filter(email=email).first()
    if user is None:
        raise CustomApiException(ErrorCodes.NOT_FOUND,message="Foydalanuvchi topilmadi.")
    if not otp:
        send_otp_email_task.delay(email)
        return {
            "message": "OTP yuborildi. Iltimos, emailingizni tekshiring."
        }
    cached_otp = UserOtp.objects.filter(email=email, otp_code=otp, is_verified=False).first()
    if cached_otp is None:
        raise CustomApiException(ErrorCodes.OTP_EXPIRED,message="OTP muddati tugagan yoki mavjud emas.")

    if cached_otp.otp_code != otp:
        raise CustomApiException(ErrorCodes.INVALID_INPUT,message="Xato kod terdingiz.")

    return {
        "message": "OTP muvaffaqiyatli tasdiqlandi."
    }


def change_password(data):
    email = data.get("email")
    new_password = data.get("new_password")
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        raise CustomApiException(ErrorCodes.NOT_FOUND,message="Foydalanuvchi topilmadi.")
    hashed_password = make_password(new_password)
    user.password = hashed_password
    user.save()
    return True



