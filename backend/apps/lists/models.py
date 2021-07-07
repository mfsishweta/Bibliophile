from django.db import models
from backend.apps.users.models import TimestampedModel, User
from backend.apps.books.models import Book
# Create your models here.


class ListType(TimestampedModel):
    type = models.CharField(max_length=25, primary_key=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "list_types"


class UserList(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    list = models.ForeignKey(ListType, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_lists"
