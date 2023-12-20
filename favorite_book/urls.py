from django.urls import path
from favorite_book.views import favorite_book, get_total_wishlist, get_wishlisted_books

app_name = 'favorite_book'

urlpatterns = [
    path('', favorite_book, name='favorite_book'),
    path('get_total_wishlist/', get_total_wishlist, name='get_total_wishlist'),
    path('get_wishlisted_books/', get_wishlisted_books, name='get_wishlisted_books'),
]