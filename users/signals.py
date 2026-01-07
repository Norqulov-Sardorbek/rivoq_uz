from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.core.files.base import ContentFile
import requests

from .models import CustomUser


@receiver(user_logged_in)
def sync_social_user_to_customuser(sender, request, user, **kwargs):
    """
    Google yoki GitHub orqali login bo‘lganda
    CustomUser jadvaliga ma’lumotlarni yozadi
    """

    email = user.email
    if not email:
        return

    # Social account (google yoki github)
    social = user.socialaccount_set.first()
    if not social:
        return

    provider = social.provider           
    data = social.extra_data              

    if provider == "google":
        first_name = data.get("given_name", "")
        last_name = data.get("family_name", "")
        avatar_url = data.get("picture")

    elif provider == "github":
        full_name = data.get("name", "") or ""
        parts = full_name.split(" ", 1)
        first_name = parts[0] if parts else ""
        last_name = parts[1] if len(parts) > 1 else ""
        avatar_url = data.get("avatar_url")

    else:
        return

    custom_user, created = CustomUser.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "is_verified": True,
        }
    )

    if not created:
        custom_user.first_name = first_name or custom_user.first_name
        custom_user.last_name = last_name or custom_user.last_name
        custom_user.is_verified = True

    if avatar_url and not custom_user.image:
        try:
            response = requests.get(avatar_url, timeout=5)
            if response.status_code == 200:
                custom_user.image.save(
                    f"{provider}_{custom_user.id}.jpg",
                    ContentFile(response.content),
                    save=False
                )
        except Exception:
            pass

    custom_user.save()
