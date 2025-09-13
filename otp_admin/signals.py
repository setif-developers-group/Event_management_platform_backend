from django.db.models import signals
from django.contrib.auth.models import User
from django.dispatch import receiver
@receiver(signals.post_save, sender=User)
def create_otp_device(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        try:
            from django_otp.plugins.otp_email.models import EmailDevice
            EmailDevice.objects.get_or_create(
                user=instance, 
                name=f"{instance.username}_email_device",
                defaults={'confirmed': True}  # You might want to set this
            )
        except Exception as e:
            # Log the error instead of failing silently
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create EmailDevice for user {instance.username}: {e}")