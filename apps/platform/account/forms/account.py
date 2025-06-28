from django import forms
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from core.models import User, Account
from django.utils.translation import gettext_lazy as _


# User update form
# ----------------------------------------------------------------------------------------------------------------------
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('email'),
        widget=forms.EmailInput(attrs={
            'class': 'text-sm font-medium bg-zinc-100 text-zinc-500',
        }),
        help_text=_('If you want to change your email, write to us!')
    )
    username = forms.CharField(
        label=_('username'),
        widget=forms.TextInput(attrs={
            'class': 'text-sm font-medium bg-zinc-100 text-zinc-500',
        }),
        help_text=_('If you want to change your username, write to us!')
    )
    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs={
            'class': 'text-sm font-medium',
        }),
    )
    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(attrs={
            'class': 'text-sm font-medium',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = 'readonly'
        self.fields['username'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = User
        fields = ('avatar', 'email', 'username', 'first_name', 'last_name',)


# Account form
# ----------------------------------------------------------------------------------------------------------------------
class AccountForm(forms.ModelForm):
    birthday = forms.DateField(
        label=_('Birthday'),
        widget=forms.DateInput(attrs={
            'placeholder': 'DD.MM.YYYY'
        }),
    )

    class Meta:
        model = Account
        fields = ('birthday', 'gender', 'bio', )


class PasswordChangeForm(BasePasswordChangeForm):
    old_password = forms.CharField(
        label=_('Old password'),
        widget=forms.PasswordInput(attrs={
            'class': 'text-sm font-medium',
        }),
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={
            'class': 'text-sm font-medium',
        }),
    )
    new_password2 = forms.CharField(
        label=_('Confirm new password'),
        widget=forms.PasswordInput(attrs={
            'class': 'text-sm font-medium',
        }),
    )
