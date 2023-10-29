from django.urls import path
from favorite_book.views import add_favorite, show_favorite

urlpatterns = [
    path('', show_favorite, name='show_favorite'),
    path('book/<int:book_id>', add_favorite, name='add_favorite'),
]