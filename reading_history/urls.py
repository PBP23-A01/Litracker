from django.urls import path
from reading_history.views import reading_history

app_name = 'reading_history'

urlpatterns = [
    path('reading_history/<int:pk>', reading_history, name='reading_history'),
]