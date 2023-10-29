from django.urls import path
from reading_history.views import reading_history, get_read_books, get_last_page

app_name = 'reading_history'

urlpatterns = [
    path('reading_history/<int:pk>', reading_history, name='reading_history'),
    path('get_read_books/', get_read_books, name='get_read_books'),
    path('get_last_page/<int:book_id>/', get_last_page, name='get_last_page'),
]