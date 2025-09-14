from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
import cloudinary.uploader
from .models import Speaker, Partner, Registration, Certificate, Notification
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_registration_badge
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
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1772cd 0%, #359aec 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .workshop-info {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #1772cd; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .button {{ display: inline-block; background: #1772cd; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Registration Confirmed!</h1>
                    <p>Welcome to SDG Skills Lab</p>
                </div>
                
                <div class="content">
                    <h2>Dear {instance.first_name},</h2>
                    
                    <p>Great news! Your registration has been <strong>confirmed</strong> for:</p>
                    
                    <div class="workshop-info">
                        <h3>📚 {instance.workshop.title}</h3>
                        <p><strong>Participant:</strong> {instance.get_full_name()}</p>
                        <p><strong>Registration ID:</strong> #{instance.id}</p>
                    </div>
                    
                    <p>🎫 Please find your personalized invitation attached to this email. Show this at the entrance to gain access to the workshop.</p>
                    
                    <p>We're excited to have you join us and look forward to seeing you there!</p>
                    
                    <div class="footer">
                        <p><strong>Best regards,</strong><br>
                        SDG Skills Lab Team</p>
                        
                        <p><em>Questions? Reply to this email and we'll help you out!</em></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create EmailMessage instance
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.email]
        )
        email.content_subtype = "html"  # Main content is now text/html
        # Attach QR code
        email.attach(f'sdg_skills_lab_{instance.workshop.title}_{instance.first_name}_{instance.last_name}.png', bg.getvalue(), 'image/png')

        # Send email
        email.send()
        
        # Create a notification record to avoid sending multiple emails
        notification = Notification.objects.create(registration=instance)
        notification.sent = True
        notification.save()