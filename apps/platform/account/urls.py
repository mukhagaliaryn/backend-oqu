from django.urls import path, re_path, include
from .views import auth


urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),

    # This is custom jwt urls...
    path('auth/jwt/create/', auth.TokenAccessAPIView.as_view()),
    path('auth/jwt/refresh/', auth.TokenRefreshView.as_view()),
    path('auth/jwt/verify/', auth.TokenVerifyAPIView.as_view()),
    re_path(r'^auth/o/(?P<provider>\S+)/$', auth.AuthProviderAPIView.as_view(), name='provider-auth'),
    path('auth/logout/', auth.LogoutAPIView.as_view()),
    # re_path(r'^auth/', include('djoser.urls.jwt')),
    # re_path(r'^auth/', include('djoser.social.urls')),
]