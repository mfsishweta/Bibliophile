from django.db import models

from apps.books.models import Book
from apps.users.models import TimestampedModel, User


class ListType(TimestampedModel):
    type = models.CharField(max_length=25, primary_key=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "list_types"


ListChoices = (('w', 'wishlist'),
               ('r', 'readlist'),
               ('s', 'shelflist')
               )


class UserList(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book, null=True)
    list = models.CharField(max_length=20, choices=ListChoices)

    class Meta:
        db_table = "user_lists"
