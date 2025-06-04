from social_core.exceptions import AuthException
from django.contrib.auth import get_user_model
User = get_user_model()


def update_google_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2' and response.get('picture'):
        user.google_avatar = response['picture']
        user.save()


def update_full_name(strategy, details, user=None, *args, **kwargs):
    if user and not user.full_name:
        full_name = details.get('fullname') or f"{details.get('first_name', '')} {details.get('last_name', '')}"
        user.full_name = full_name.strip()
        user.save()


def validate_google_email_association(strategy, details, user=None, backend=None, *args, **kwargs):
    email = details.get('email')

    if not email:
        raise AuthException(backend, "Email мәліметі алынбады.")

    try:
        existing_user = User.objects.get(email=email)
    except User.DoesNotExist:
        return

    if not existing_user.social_auth.filter(provider='google-oauth2').exists():
        raise AuthException(backend, f"'{email}' адресі жүйеде бұрыннан тіркелген. Google арқылы кіру рұқсат етілмеген.")
