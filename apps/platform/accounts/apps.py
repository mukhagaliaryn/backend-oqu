from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.platform.accounts'

    def ready(self):
        import apps.platform.accounts.signals
