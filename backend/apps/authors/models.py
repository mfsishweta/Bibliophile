from django.db import models
from apps.users.models import TimestampedModel

# Create your models here.


class Author(TimestampedModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "authors"
