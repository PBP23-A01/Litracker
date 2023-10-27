from django.urls import path
from upvote_book.views import upvote_book

app_name = 'upvote_book'

urlpatterns = [
    path('', upvote_book, name='upvote_book'),
]
