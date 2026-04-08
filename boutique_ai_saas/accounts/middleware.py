from django.utils import translation

from .models import UserProfile


class ProfileLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user).first()
            if profile and profile.language:
                translation.activate(profile.language)
                request.LANGUAGE_CODE = profile.language
        response = self.get_response(request)
        translation.deactivate()
        return response

