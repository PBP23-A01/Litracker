from django.urls import path
from upvote_book.views import upvote_book, toggle_upvote_flutter

app_name = 'upvote_book'

urlpatterns = [
    path('', upvote_book, name='upvote_book'),
    path('toggle_upvote_flutter/<int:book_id>/', toggle_upvote_flutter, name='toggle_upvote_flutter'),
]