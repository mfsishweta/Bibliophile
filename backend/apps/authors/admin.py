from django.contrib import admin
from .models import *

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    model = Author


admin.site.register(Author, AuthorAdmin)