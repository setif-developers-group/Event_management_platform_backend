from django.contrib import admin
from django_otp.admin import OTPAdminSite

# Replace default admin site with OTP admin site
admin.site.__class__ = OTPAdminSite