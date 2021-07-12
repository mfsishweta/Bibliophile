from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.authors.models import Author
from apps.users.models import TimestampedModel


# Create your models here.


class Genre(models.Model):
    category = models.CharField(max_length=25)

    class Meta:
        db_table = 'genres'


class Book(TimestampedModel):
    volume_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    authors = models.ManyToManyField(Author, null=True, blank=True)

    class Meta:
        db_table = "books"


