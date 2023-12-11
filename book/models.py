from django.db import models

class Book(models.Model):
    isbn = models.CharField(max_length=255, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    image_url_s = models.TextField(null=True, blank=True)
    image_url_m = models.TextField(null=True, blank=True)
    image_url_l = models.TextField(null=True, blank=True)

class BookVotes(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='votes')
    total_votes = models.IntegerField(default=0)

class BookWishlist(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='wishlist')
    total_wishlist = models.IntegerField(default=0)
