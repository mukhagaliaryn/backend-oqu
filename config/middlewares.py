from django.shortcuts import redirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


# Redirect auth
class RedirectAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = ['/accounts/login/', '/accounts/register/']
        if request.user.is_authenticated and request.path in restricted_paths:
            return redirect('workspace')
        return self.get_response(request)


# Locale
class CustomLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = request.session.get('django_language') or request.COOKIES.get('django_language')

        if not language:
            language = 'kk'

        translation.activate(language)
        request.LANGUAGE_CODE = language