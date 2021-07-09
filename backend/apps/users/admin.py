from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


# Register your models here.


class UserAdmin(BaseUserAdmin):
    model = User
    search_fields = ['first_name', 'username']
    list_display = ['first_name', 'last_name', 'username', 'is_active']


admin.site.register(User, UserAdmin)
