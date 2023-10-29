from django.urls import path
from book.views import get_books, show_homepage, upvote_book, search_books, wishlist_book, simpan_last_page, last_page

app_name = 'book'

urlpatterns = [
    path('api/book/', get_books, name='get_books'),
    path('', show_homepage, name='show_homepage'),
    path('book/search-books/', search_books, name='search_books'),
    path('upvote_book/<int:book_id>/', upvote_book, name='upvote_book'),
    path('last_page',last_page, name="last_page"),
    path('simpan_last_page/<int:book_id>/', simpan_last_page, name='simpan_last_page'),
    path('wishlist_book/<int:book_id>/', wishlist_book, name='wishlist_book')
]
