from django.urls import path
from review_book.views import show_review, add_review, add_review_ajax, create_review, get_book_reviews, post_book_review

app_name = 'review_book'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('add_review.html', add_review, name='add_review'),
    
    path('create-review-ajax/', add_review_ajax, name='add_review_ajax'),
    path('create-review', create_review, name='create_review'),
    path('post_book_reviews/<int:book_id>/', post_book_review, name='post_book_reviews'),
    path('get_book_reviews/<int:book_id>/', get_book_reviews, name='get_book_reviews'),

]