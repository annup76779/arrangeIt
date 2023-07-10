from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_role': user.role,
        'expires_in': refresh.lifetime,
        "email": user.email,
        "name": user.first_name,
        "join_code": user.join_code if user.role == 1 else ""
    }