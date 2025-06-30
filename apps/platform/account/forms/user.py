from django import forms
from core.models import User, Account


# User update form
# ----------------------------------------------------------------------------------------------------------------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'avatar', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True


# Account form
# ----------------------------------------------------------------------------------------------------------------------
class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('birthday', 'gender', 'bio', )

