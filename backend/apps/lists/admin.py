from django.contrib import admin

from .models import *


class ListTypeAdmin(admin.ModelAdmin):
    model = ListType


class UserListAdmin(admin.ModelAdmin):
    model = UserList
    search_fields = ['user']
    # filter_horizontal = ['book']
    list_display = ['id', 'user', 'list']


admin.site.register(ListType, ListTypeAdmin)
admin.site.register(UserList, UserListAdmin)
