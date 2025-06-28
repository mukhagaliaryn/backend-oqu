from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from core.models import User


# User login form
# ----------------------------------------------------------------------------------------------------------------------
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('email'),
        widget=forms.EmailInput(attrs={
            'class': 'text-sm font-medium',
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'text-sm font-medium'
        })
    )


# User register form
# ----------------------------------------------------------------------------------------------------------------------
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return username.lower()
