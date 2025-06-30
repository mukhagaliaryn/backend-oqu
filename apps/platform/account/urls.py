from django.urls import path
from django.contrib.auth import views as auth_views
from .views import auth, user


urlpatterns = [
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='app/platform/account/auth/password_reset.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/platform/account/auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('profile/', user.profile, name='profile'),
    path('account/', user.account, name='account'),
    path('subscriptions/', user.subscriptions, name='subscriptions'),
    path('payments/', user.payments, name='payments'),
    path('settings/', user.settings, name='settings'),
    path('password_change/', user.change_password, name='password_change'),
]
