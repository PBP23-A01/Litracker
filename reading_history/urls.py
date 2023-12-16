from django.urls import path
from reading_history.views import history_book, show_history, fetch_history, delete_history_entry, edit_page_number

app_name = 'reading_history'

urlpatterns = [
    path('history_book/', history_book, name='history_book'),
    path('show_history/', show_history, name='show_history'),
    path('fetch_history/', fetch_history, name='fetch_history'),
    path('delete_history_entry/', delete_history_entry, name='delete_history_entry'),
    path('edit_page_number/', edit_page_number, name='edit_page_number')
]