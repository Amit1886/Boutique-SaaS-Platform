from .models import UserProfile


def user_context(request):
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
    return {"user_profile": profile}

