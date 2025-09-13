from django.apps import AppConfig


class AppModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_models'
    def ready(self):
        import app_models.signals
