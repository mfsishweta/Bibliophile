from django.db import models
from apps.users.models import TimestampedModel, User
from apps.books.models import Book
# Create your models here.


class UserBookRatingReviews(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete= models.CASCADE)
    ratings = models.DecimalField(max_digits=4,decimal_places=2, null=True, blank=True)
    reviews = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "user_book_ratings_reviews"
