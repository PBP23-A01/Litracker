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



class MyUpvoteListFlutter(models.Model):
    me = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # 1 dari banyak orang
    books = models.ManyToManyField(Book, related_name='upvoted_books') # Banyak buku
    reasoning = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class UpvotedbyUsersFlutter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    users = models.ManyToManyField(UserProfile)
    created = models.DateTimeField(auto_now_add=True)
