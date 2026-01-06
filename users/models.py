from django.db import models
from core.models.basemodel import SafeBaseModel

class CustomUser(SafeBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    telegram_link = models.CharField(max_length=255, null=True, blank=True)
    git_link = models.CharField(max_length=255, null=True, blank=True)
    linkedin_link = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class UserOtp(SafeBaseModel):
    email = models.EmailField()
    otp_code = models.CharField(max_length=5)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.email} - {self.otp_code}"

    class Meta:
        verbose_name = "Foydalanuvchi OTP"
        verbose_name_plural = "Foydalanuvchi OTPlari"
        