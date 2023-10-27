from django.db import models
from book.models import Book  # Mengimport model Book yang telah Anda definisikan sebelumnya
from authentication.models import UserProfile

class ReviewBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

   