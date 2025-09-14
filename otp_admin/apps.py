from django.apps import AppConfig

from decouple import config
from django.db.models.signals import post_migrate
def create_admin(sender, **kwargs):
    '''
    Create admin user if not exists
    '''
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username=config('ADMIN_USERNAME', 'aymen')).exists():
        User.objects.create_superuser(username=config('ADMIN_USERNAME','aymen'), email=config('ADMIN_EMAIL','aymen_merad@proton.me'), password=config('ADMIN_PASSWORD','admin'))


class OtpAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otp_admin'
    def ready(self):
        import otp_admin.signals
        post_migrate.connect(create_admin, sender=self)