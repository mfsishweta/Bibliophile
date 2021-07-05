from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimestampedModel):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    username = models.CharField(max_length=70, unique=True)
    # profile_pic = models.ImageField(null=True, blank=True)
    friend = models.ManyToManyField('self')
    short_desc = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    reset_password = models.BooleanField(default=True)

    class Meta:
        db_table = "users"




