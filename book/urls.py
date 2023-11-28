from django.urls import path
from book.views import get_books, show_homepage, upvote_book, search_books, wishlist_book, tambah_buku, history_book

app_name = 'book'

urlpatterns = [
    path('api/book/', get_books, name='get_books'),
    path('', show_homepage, name='show_homepage'),
    path('book/search-books/', search_books, name='search_books'),
    path('upvote_book/<int:book_id>/', upvote_book, name='upvote_book'),
    path('wishlist_book/<int:book_id>/', wishlist_book, name='wishlist_book'),
    path('tambah_buku/', tambah_buku, name='tambah_buku'),
    path('history_book/<int:book_id>', history_book, name='history_book')
]
