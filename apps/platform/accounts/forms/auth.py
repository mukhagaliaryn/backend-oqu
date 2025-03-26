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
            'placeholder': 'name@example.com',
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
    email = forms.EmailField(
        label=_('email'),
        widget=forms.EmailInput(attrs={
            'class': 'text-sm font-medium',
            'placeholder': 'example@gmail.com'
        }),
    )
    username = forms.CharField(
        label=_('username'),
        widget=forms.TextInput(attrs={
            'class': 'text-sm font-medium',
            'placeholder': 'my.username'
        }),
    )
    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs={
            'class': 'text-sm font-medium',
            'placeholder': _('Write your first name')
        }),
    )
    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(attrs={
            'class': 'text-sm font-medium',
            'placeholder': _('Write your last name')
        }),
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'text-sm font-medium',
            'placeholder': _('Come up with a strong password')
        }),
    )
    password2 = forms.CharField(
        label=_('Password confirm'),
        widget=forms.PasswordInput(attrs={
            'class': 'text-sm font-medium',
            'placeholder': _('Repeat the password')
        }),
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', )
