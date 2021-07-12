from django.contrib import admin

# Register your models here.
from apps.coreauth.models import OTPAuthentication


class OTPAuthenticationAdmin(admin.ModelAdmin):
    model = OTPAuthentication
    search_fields = ['user']
    list_display = ['user','otp','expire_at']

admin.site.register(OTPAuthentication, OTPAuthenticationAdmin)