from django.urls import path
from reading_history.views import show_history

app_name = 'reading_history'

urlpatterns = [
    path('', show_history, name='show_history'),
]