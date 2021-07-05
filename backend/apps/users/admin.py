from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserAdmin(BaseUserAdmin):
    model = User
    search_fields = ['first_name']


admin.site.register(User, UserAdmin)




