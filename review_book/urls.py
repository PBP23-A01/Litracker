from django.urls import path
from review_book.views import show_review, add_review, add_review_ajax, show_create_review

app_name = 'review_book'

urlpatterns = [
    path('', show_review, name='show_review'),
    path('add_review/', add_review, name='add_review'),
    
    path('create-review-ajax/', add_review_ajax, name='add_review_ajax'),
    path('show_create_review/', show_create_review, name='show_create_review'),
]