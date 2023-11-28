from django.urls import path
from reading_history.views import history_book, show_history

app_name = 'reading_history'

urlpatterns = [
    path('history_book', history_book, name='history_book'),
    path('show_history', show_history, name='show_history'),

]