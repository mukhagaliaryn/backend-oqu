from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User


# Account model
# ----------------------------------------------------------------------------------------------------------------------
# Account
class Account(models.Model):
    ACCOUNT_TYPE = (
        ('default', _('User')),
        ('student', _('Student')),
        ('teacher', _('Teacher')),
    )
    GENDER = (
        ('undefined', _('Undefined')),
        ('male', _('Male')),
        ('female', _('Female')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    account_type = models.CharField(
        _('Account type'), max_length=64,
        choices=ACCOUNT_TYPE, default='default'
    )
    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=64, choices=GENDER, default='undefined')
    bio = models.TextField(_('Bio'), max_length=255, blank=True, null=True)
    last_account_update = models.DateTimeField(_('Last account update'), null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
