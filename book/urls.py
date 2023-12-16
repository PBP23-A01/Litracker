from django.urls import path
from book.views import get_books, show_homepage, upvote_book, search_books, wishlist_book, tambah_buku, upvote_book_mobile, wishlist_book_mobile, add_book_mobile, edit_book_mobile, delete_book_mobile
from reading_history.views import history_book

app_name = 'book'

urlpatterns = [
    path('api/book/', get_books, name='get_books'),
    path('api/book/edit/<int:pk>/', edit_book_mobile, name='edit_book'),
    path('api/book/delete/<int:pk>/', delete_book_mobile, name='delete_book'),
    path('', show_homepage, name='show_homepage'),
    path('book/search-books/', search_books, name='search_books'),
    path('upvote_book/<int:book_id>/', upvote_book, name='upvote_book'),
    path('wishlist_book/<int:book_id>/', wishlist_book, name='wishlist_book'),
    path('upvote_book_mobile/<int:book_id>/', upvote_book_mobile, name='upvote_book_mobile'),
    path('wishlist_book_mobile/<int:book_id>/', wishlist_book_mobile, name='wishlist_book_mobile'),
    path('tambah_buku/', tambah_buku, name='tambah_buku'),
    path('add-book-mobile/', add_book_mobile, name='add_book_mobile'),
    path('history_book/', history_book, name='history_book')
]
