from django.db import models

# Create your models here.
from apps.users.models import User


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class OTPAuthentication(TimestampedModel):
    user = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    otp = models.CharField(max_length=20)
    expire_at = models.DateTimeField()

    db_table = 'otp_authentication'
