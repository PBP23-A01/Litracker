from django.db import models
from django.contrib.auth.models import User
from authentication.models import UserProfile
from book.models import Book


class Upvote(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    upvote_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'book')