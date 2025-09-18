from django.contrib import admin, messages

# Register your models here.

from .models import Speaker, Partner, Workshop, Registration, Certificate, Notification, UploadModeslByFile, TargetModel


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner')
    search_fields = ('name', 'bio', 'partner__name', 'workshops__title', 'workshops__date')
    list_filter = ('name',)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name','short_description', 'website')
    search_fields = ('name',)

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title','description', 'speaker__name', 'partner__name')
    list_filter = ('date', 'speaker', 'partner')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'workshop')
    search_fields = ('first_name', 'last_name', 'email', 'workshop__title')
    list_filter = ('workshop', 'confirmed', 'registration_date')
    def confirm_registration(self, request, queryset):
        count = 0
        for registration in queryset:
            registration.confirmed = True
            registration.save()  # This will trigger the post_save signal
            count += 1
        self.message_user(request, f"{count} registrations confirmed.")

    confirm_registration.short_description = "Confirm selected registrations"
    actions = [confirm_registration]
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('registration', 'issued_date')
    search_fields = ('registration__first_name', 'registration__last_name')
    list_filter = ('issued_date',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('registration', 'sent_date')
    search_fields = ('registration__first_name', 'registration__last_name')
    list_filter = ('sent_date',)


@admin.register(UploadModeslByFile)
class UploadModeslByFileAdmin(admin.ModelAdmin):
    list_display = ('target_model', 'file', 'upload_date')
    search_fields = ('upload_date',)
    list_filter = ('target_model', 'upload_date')
    