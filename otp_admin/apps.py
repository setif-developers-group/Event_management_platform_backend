from django.apps import AppConfig
from django.contrib.auth import get_user_model
from decouple import config
def create_admin():
    '''
    Create admin user if not exists
    '''
    User = get_user_model()
    if not User.objects.filter(username=config('ADMIN_USERNAME', 'aymen')).exists():
        User.objects.create_superuser(username=config('ADMIN_USERNAME','aymen'), email=config('ADMIN_EMAIL','aymen_merad@proton.me'), password=config('ADMIN_PASSWORD','admin'))


class OtpAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otp_admin'
    def ready(self):
        import otp_admin.signals
        create_admin()