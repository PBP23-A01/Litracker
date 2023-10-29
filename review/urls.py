from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('', views.show_review, name='show_review'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add_review/<int:book_id>/', views.add_review, name='add_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
