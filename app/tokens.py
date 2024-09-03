from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # Add custom claims here
    refresh['username'] = user.username
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }