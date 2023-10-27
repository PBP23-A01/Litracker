from django.db import models
from django.contrib.auth.models import User
from authentication.models import UserProfile
from book.models import Book

# Create your models here.
class ReadingHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    last_page = models.PositiveIntegerField(default=0)
    date_opened = models.DateField(auto_now_add=True)