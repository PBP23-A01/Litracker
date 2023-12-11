from django.urls import path
from upvote_book.views import upvote_book, get_total_votes

app_name = 'upvote_book'

urlpatterns = [
    path('', upvote_book, name='upvote_book'),
    path('get_total_votes/', get_total_votes, name='get_total_votes')
]