from django.urls import path
from favorite_book.views import favorite_book

app_name = 'favorite_book'

urlpatterns = [
    path('', favorite_book, name='favorite_book'),
]