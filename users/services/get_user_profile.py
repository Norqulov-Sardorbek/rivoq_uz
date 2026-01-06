from users.models import CustomUser as User





def get_user_profile(user_id):
    try:
        user = User.objects.get(id=user_id)
        return {
            "id": user.id,
            "email": user.email,
        }
    except User.DoesNotExist:
        return None