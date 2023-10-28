from django.urls import path
from book.views import get_books, show_homepage, upvote_book

app_name = 'book'

urlpatterns = [
    path('api/book/', get_books, name='get_books'),
    path('', show_homepage, name='show_homepage'),
    path('upvote_book/<int:book_id>/', upvote_book, name='upvote_book'),
]
