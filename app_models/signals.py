from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
import cloudinary.uploader
from .models import Speaker, Partner, Registration, Certificate, Notification
from django.core.mail import EmailMessage
from django.conf import settings
import qrcode
from io import BytesIO
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
def send_confirmation_email(sender, instance, created, **kwargs):

    if instance.confirmed and not Notification.objects.filter(registration=instance).exists():
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'Registration ID: {instance.id}, Name: {instance.first_name} {instance.last_name}, Workshop: {instance.workshop.title}')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code to BytesIO buffer
        qr_buffer = BytesIO()
        img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)  # Move to the beginning of the buffer
        
        # Create email
        subject = 'Workshop Registration Confirmed'
        message = f'Dear {instance.first_name},\n\nYour registration for the workshop "{instance.workshop.title}" has been confirmed.\n\nBest regards,\nSDG Skills Lab Team'
        
        # Create EmailMessage instance
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.email]
        )
        
        # Attach QR code
        email.attach(f'registration_qr_{instance.id}.png', qr_buffer.getvalue(), 'image/png')
        
        # Send email
        email.send()
        
        # Create a notification record to avoid sending multiple emails
        notification = Notification.objects.create(registration=instance)
        notification.save()