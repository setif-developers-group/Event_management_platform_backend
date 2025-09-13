from django.apps import AppConfig


class OtpAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otp_admin'
    def ready(self):
        import otp_admin.signals