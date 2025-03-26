from django.urls import path
from django.contrib.auth import views as auth_views
from .views import auth, account
from apps.platform.accounts.forms.auth import UserLoginForm


urlpatterns = [
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='src/pages/accounts/auth/login.html',
        authentication_form=UserLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='src/pages/accounts/auth/password_reset.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='src/pages/accounts/auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='src/pages/accounts/auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='src/pages/accounts/auth/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('profile/', account.profile, name='profile'),
    path('account/', account.account, name='account'),
    path('subscriptions/', account.subscriptions, name='subscriptions'),
    path('payments/', account.payments, name='payments'),
    path('settings/', account.settings, name='settings'),
    path('password_change/', account.change_password, name='password_change'),
]
