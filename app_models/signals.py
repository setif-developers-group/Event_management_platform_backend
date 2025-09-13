from django.db.models.signals import post_delete
from django.dispatch import receiver
import cloudinary.uploader
from .models import Speaker, Partner

@receiver(post_delete, sender=Speaker)
def delete_speaker_image(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)

# Signal to delete the associated image from Cloudinary when a Partner is deleted
@receiver(post_delete, sender=Partner)
def delete_partner_logo(sender, instance, **kwargs):
    if instance.logo:
        cloudinary.uploader.destroy(instance.logo.public_id)