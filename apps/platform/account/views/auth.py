from django.contrib.auth.views import PasswordResetConfirmView as BasePasswordResetConfirmView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from apps.platform.account.forms.auth import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


# login page
# ----------------------------------------------------------------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('workspace')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('workspace')
        else:
            messages.error(request, _('Incorrect email or password'))
    else:
        form = AuthenticationForm()

    return render(request, 'app/platform/account/auth/login.html', {'form': form})


# register page
# ----------------------------------------------------------------------------------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('workspace')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('workspace')
        else:
            messages.error(request, _('An error occurred during the registration process'))
    else:
        form = UserRegisterForm()

    return render(request, 'app/platform/account/auth/register.html', {'form': form})



# password reset confirm page
# ----------------------------------------------------------------------------------------------------------------------
class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name='app/platform/account/auth/password_reset_confirm.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, _('Password reset successfully'))
        return redirect('workspace')


# logout
# ----------------------------------------------------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')