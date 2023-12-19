from django.urls import path
from review_book.views import delete_book_review, get_all_reviews, show_review, add_review, add_review_ajax, \
    create_review, get_book_reviews, post_book_review, \
 get_snippet_reviews_without_rating, get_snippet_reviews_without_timestamp

app_name = 'review_book'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('add_review.html', add_review, name='add_review'),
    path('get_all_reviews/', get_all_reviews, name='get_all_reviews'),
    path('create-review-ajax/', add_review_ajax, name='add_review_ajax'),
    path('create-review', create_review, name='create_review'),
    path('post_book_reviews/<int:book_id>/', post_book_review, name='post_book_reviews'),
    path('get_book_reviews/<int:book_id>/', get_book_reviews, name='get_book_reviews'),
    path('delete_book_reviews/<int:review_id>/', delete_book_review, name='delete_book_reviews'),
    path('get_snippet_reviews_without_rating', get_snippet_reviews_without_rating, name='get_snippet_reviews_without_rating'),
    path('get_snippet_reviews_without_timestamp', get_snippet_reviews_without_timestamp, name='get_snippet_reviews_without_timestamp'),
    
]