from django.urls import path
from book.views import get_books, show_homepage, find_book

app_name = 'book'

urlpatterns = [
    path('api/book/', get_books, name='get_books'),
    path('', show_homepage, name='show_homepage'),
    path('find-book/', find_book, name='find_book'),
]