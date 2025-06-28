from django.contrib import admin
from core.models import Subscription


# Subscription admin
# ----------------------------------------------------------------------------------------------------------------------
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_default', 'is_unlimited', 'is_active', )
    list_filter = ('is_default', 'is_unlimited', 'is_active', )
    search_fields = ('name', )


# registrations
# ----------------------------------------------------------------------------------------------------------------------
admin.site.register(Subscription, SubscriptionAdmin)