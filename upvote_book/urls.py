from django.urls import path
from upvote_book.views import get_upvoted_books, upvote_book, toggle_upvote_flutter, get_upvoting_users

app_name = 'upvote_book'

urlpatterns = [
    path('', upvote_book, name='upvote_book'),
    path('toggle_upvote_flutter/<int:book_id>/', toggle_upvote_flutter, name='toggle_upvote_flutter'),    
    path('get_upvoting_users/<int:book_id>/', get_upvoting_users, name='get_upvoting_users'),
    path('get_upvoted_books/', get_upvoted_books, name='get_upvoted_books'),
]