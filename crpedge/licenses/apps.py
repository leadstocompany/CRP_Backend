from django.apps import AppConfig

class LicensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'licenses'

    def ready(self):
        # Register signal handlers
        import licenses.signals
