from django.contrib import admin
from .models import *
# Register your models here.


class UserBookRatingReviewsAdmin(admin.ModelAdmin):
    model = UserBookRatingReviews


admin.site.register(UserBookRatingReviews, UserBookRatingReviewsAdmin)

# Register your models here.
