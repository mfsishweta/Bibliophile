from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    model = User
    search_fields = ['first_name', 'username']
    filter_horizontal = ('friend',)
    list_display = ['first_name', 'last_name', 'username', 'is_active']


class FriendRequestAdmin(admin.ModelAdmin):
    model = FriendRequest
    # search_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user']


admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
