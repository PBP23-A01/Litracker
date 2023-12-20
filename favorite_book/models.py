from django.db import models
from book.models import Book

from authentication.models import UserProfile

# Create your models here.


class WishlistBook(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

