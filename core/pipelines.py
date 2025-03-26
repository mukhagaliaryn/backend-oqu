
def update_google_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2' and response.get('picture'):
        user.google_avatar = response['picture']
        user.save()