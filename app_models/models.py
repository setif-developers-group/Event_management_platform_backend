from django.db import models
from django.core.validators import MinLengthValidator
from cloudinary.models import CloudinaryField
import cloudinary.uploader

# Create your models here.

class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = CloudinaryField(folder='sdg_skills_lab/Partners_logo', blank=True, null=True)
    short_description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_partner_name')
        ]

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    image = CloudinaryField(folder='sdg_skills_lab/Speakers_imgs', blank=True, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'bio'], name='unique_speaker_fullinfo')
        ]
class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    duration = models.SmallIntegerField()
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True, blank=True, related_name='workshops')
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='workshops')

    def __str__(self):
        return self.title
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_workshop_title')
        ]

class AttendanceType(models.TextChoices):
    ONLINE = "online", "online"
    ON_SITE = "on-site", "On-site"
class Registration(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    attendance_type = models.CharField(max_length=10, choices=AttendanceType.choices, default=AttendanceType.ON_SITE)
    registration_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'workshop'],
                name='unique_email_workshop'
            )
        ]
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.workshop.title}"
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Certificate(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now_add=True)
    certificate_file = CloudinaryField(folder='sdg_skills_lab/Certificates', blank=True, null=True)
    def __str__(self):
        return f"Certificate for {self.registration.first_name} {self.registration.last_name} - {self.registration.workshop.title}"


class Notification(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.registration.first_name} {self.registration.last_name} - {self.registration.workshop.title}"
    
class TargetModel(models.TextChoices):
    Workshops = "workshop"
    Partners = "partner"
    Speakers = "speaker"

class UploadModeslByFile(models.Model):
    target_model = models.CharField(max_length=20, choices=TargetModel.choices, default=TargetModel.Partners)
    file = models.FileField(null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload for {self.target_model} - {self.upload_date} - {self.pk}"