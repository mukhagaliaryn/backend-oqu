from django.contrib import admin
from core.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'birthday', )
    list_filter = ('account_type', )


# admin.site.register(Account, AccountAdmin)