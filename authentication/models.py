from django.db import models
from django.contrib.auth.models import User
from book.models import Book


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    books = models.ManyToManyField(Book)
    upvoted_books = models.ManyToManyField(Book, related_name="upvoters", blank=True)
    wishlist_books = models.ManyToManyField(Book, related_name="wishlists", blank=True)