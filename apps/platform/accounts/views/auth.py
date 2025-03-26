from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.platform.accounts.forms.auth import UserRegisterForm


# Signup
# ----------------------------------------------------------------------------------------------------------------------
class RegisterView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'src/pages/accounts/auth/register.html'
