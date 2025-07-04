from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


# User model
# ----------------------------------------------------------------------------------------------------------------------
# User manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):

        if not username:
            raise ValueError(_('The user must have an username'))
        if not email:
            raise ValueError(_('The user must have an email address'))

        email = self.normalize_email(email)
        user = self.model(username=username.lower(), email=email.lower(), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        user = self.create_user(username, email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# User
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), max_length=128, unique=True)
    username = models.CharField(
        _('username'), max_length=128, unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    first_name = models.CharField(_('First name'), max_length=128)
    last_name = models.CharField(_('Last name'), max_length=128)
    avatar = models.ImageField(_('Avatar'), upload_to='core/models/users/', blank=True, null=True)
    google_avatar = models.URLField(_('Google avatar'), blank=True, null=True)
    is_staff = models.BooleanField(
        verbose_name=_("staff status"), default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"), default=True,
        help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now=True)
    last_profile_update = models.DateTimeField(_('Last user update'), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name' ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
