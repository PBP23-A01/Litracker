from django.urls import path,include
from book.views import get_books, show_homepage, upvote_book, search_books

app_name = 'book'

urlpatterns = [
    path('api/book/', get_books, name='get_books'),
    path('', show_homepage, name='show_homepage'),
    path('search-books/', search_books, name='search_books'),
    path('upvote_book/<int:book_id>/', upvote_book, name='upvote_book'),
    path('add_favorite/', include('favorite_book.urls')),
]
