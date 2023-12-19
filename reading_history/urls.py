from django.urls import path
from reading_history.views import delete_reading_history, history_book, show_history, fetch_history, get_all_reading_histories, get_reading_history, post_reading_history

app_name = 'reading_history'

urlpatterns = [
    path('history_book/', history_book, name='history_book'),
    path('show_history/', show_history, name='show_history'),
    path('fetch_history/', fetch_history, name='fetch_history'),
    path('get_all_reading_history/', get_all_reading_histories, name='get_all_reading_histories'),
    path('get_reading_history/<int:book_id>', get_reading_history, name='get_reading_history'),
    path('post_reading_history/<int:book_id>', post_reading_history, name='post_reading_history'),
    path('delete_reading_history/<int:history_id>/', delete_reading_history, name='delete_reading_history'),
]