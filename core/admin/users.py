from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdminMixin
from core.models import User, Account, UserSubscription, UserPayment


# User admin
# ----------------------------------------------------------------------------------------------------------------------
# Account
class AccountInline(SummernoteModelAdminMixin, admin.StackedInline):
    model = Account
    extra = 0


# UserSubscription
class UserSubscriptionInline(admin.TabularInline):
    model = UserSubscription
    extra = 0


# UserPayment
class UserPaymentInline(admin.TabularInline):
    model = UserPayment
    extra = 0


# User
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', )
    list_filter = ('is_active', 'is_staff', 'is_superuser', )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal data'), {'fields': ('first_name', 'last_name', 'avatar', 'google_avatar', 'last_login',)}),
        (_('Permissions'), {'fields': ('user_permissions', 'is_active', 'is_staff', 'is_superuser', )}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ('wide', ),
                "fields": ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', ),
            },
        ),
    )
    filter_horizontal = ('user_permissions', )
    inlines = [AccountInline, UserSubscriptionInline, UserPaymentInline ]


# registrations
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
