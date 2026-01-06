from users.models import UserOtp, CustomUser 
from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException





def verify_otp(email, otp):
    cached_otp = UserOtp.objects.filter(email=email, otp_code=otp, is_verified=False).first()
    if cached_otp is None:
        raise CustomApiException(ErrorCodes.OTP_EXPIRED,message="OTP muddati tugagan yoki mavjud emas.")

    if cached_otp.otp_code != otp:
        raise CustomApiException(ErrorCodes.INVALID_INPUT,message="Xato kod terdingiz.")

    user= CustomUser.objects.filter(email=email).first()
    if user is None:
        user = CustomUser.objects.create(email=email)
    user.is_verified = True
    user.save()
    cached_otp.is_verified = True
    cached_otp.save()
    return True
    