from django.db import models
from authentication.models import UserProfile
from book.models import Book

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_written')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()  # Ganti nama kolom ke "content"
    created_at = models.DateTimeField(auto_now_add=True)
