from django.urls import path
from review_book.views import show_review

app_name = 'review_book'

urlpatterns = [
    path('', show_review, name='show_review'),
]