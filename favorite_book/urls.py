from django.urls import path
from favorite_book.views import favorite_book, get_total_wishlist

app_name = 'favorite_book'

urlpatterns = [
    path('', favorite_book, name='favorite_book'),
    path('get_total_wishlist/', get_total_wishlist, name='get_total_wishlist'),
]