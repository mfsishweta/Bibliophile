from django.contrib import admin
from .models import *
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ['volume_id', 'title', 'publish_date']
    list_display = ['title', 'publish_date','volume_id']


class GenreAdmin(admin.ModelAdmin):
    model = Genre

admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
