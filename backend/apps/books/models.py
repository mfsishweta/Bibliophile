from django.db import models
from apps.users.models import TimestampedModel
from apps.authors.models import Author
# Create your models here.


class Genre(models.Model):
    category = models.CharField(max_length=25)

    class Meta:
        db_table = 'genres'


class Book(TimestampedModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "books"


class BookAuthor(TimestampedModel):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = "books_authors"


