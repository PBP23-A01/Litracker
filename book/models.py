from django.db import models

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=255, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    image_url_s = models.TextField(null=True, blank=True)
    image_url_m = models.TextField(null=True, blank=True)
    image_url_l = models.TextField(null=True, blank=True)