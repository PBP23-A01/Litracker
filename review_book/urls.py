from django.urls import path
from review_book.views import show_review, add_review, add_review_ajax

app_name = 'review_book'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('add_review.html', add_review, name='add_review'),
    
    path('create-review-ajax/', add_review_ajax, name='add_review_ajax')
]