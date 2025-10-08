from django.db.models.signals import post_delete,post_save, pre_save
from django.dispatch import receiver
import cloudinary.uploader
from .models import Speaker, Partner, Registration, Certificate, Notification, Workshop, TargetModel, UploadModeslByFile,Attendance, WorkshopCertificate
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_registration_badge, sent_email
from .utils import create_partners_from_file, create_speakers_from_file, create_workshops_from_file, generate_confirmation_email


@receiver(post_delete, sender=Speaker)
def delete_speaker_image(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)

# Signal to delete the associated image from Cloudinary when a Partner is deleted
@receiver(post_delete, sender=Partner)
def delete_partner_logo(sender, instance, **kwargs):
    if instance.logo:
        cloudinary.uploader.destroy(instance.logo.public_id)

# Signal to delete the associated certificate file from Cloudinary when a Certificate is deleted
@receiver(post_delete, sender=Certificate)
def delete_certificate_file(sender, instance, **kwargs):
    if instance.certificate_file:
        cloudinary.uploader.destroy(instance.certificate_file.public_id)
    
@receiver(post_save, sender=Registration)
def send_confirmation_email(sender, instance: Registration, created, **kwargs):

    if instance.confirmed and not Notification.objects.filter(registration=instance).exists():
        bg = generate_registration_badge(instance)
        # Create email
        subject = 'Workshop Registration Confirmed'
        html_message =  generate_confirmation_email(instance)
        sent_email(
            to_email=instance.email,
            subject=subject,
            body=html_message,
            attachments=[{
                'filename': f'sdg_skills_lab_{instance.workshop.title}_{instance.first_name}_{instance.last_name}_invitation.png',
                'content': bg.getvalue(),
                'mimetype': 'image/png'
            }]
        )

        # Create a notification record to avoid sending multiple emails
        notification = Notification.objects.create(registration=instance)
        notification.sent = True
        notification.save()


@receiver(pre_save, sender=UploadModeslByFile)
def create_target_model(sender, instance, **kwargs):
    
    if instance.file:
        if instance.target_model == TargetModel.Workshops:
            create_workshops_from_file(instance.file)
        elif instance.target_model == TargetModel.Partners:
            create_partners_from_file(instance.file)
        elif instance.target_model == TargetModel.Speakers:
            create_speakers_from_file(instance.file)
        instance.file = None

@receiver(pre_save, sender=WorkshopCertificate)
def create_workshop_certificate(sender, instance, **kwargs):
    if not instance.certificate_file:
        workshop: Workshop = instance.workshop
        
                