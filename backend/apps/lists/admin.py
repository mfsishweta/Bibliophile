from django.contrib import admin
from .models import *
# Register your models here.


class ListTypeAdmin(admin.ModelAdmin):
    model = ListType


class UserListAdmin(admin.ModelAdmin):
    model = UserList


admin.site.register(ListType, ListTypeAdmin)
admin.site.register(UserList, UserListAdmin)
