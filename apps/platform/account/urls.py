from django.urls import path
from django.contrib.auth import views as auth_views
from .views import auth, account


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
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/platform/account/auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/platform/account/auth/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('profile/', account.profile, name='profile'),
    path('account/', account.account, name='account'),
    path('subscriptions/', account.subscriptions, name='subscriptions'),
    path('payments/', account.payments, name='payments'),
    path('settings/', account.settings, name='settings'),
    path('password_change/', account.change_password, name='password_change'),
]
