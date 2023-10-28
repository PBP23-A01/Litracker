from django.forms import ModelForm
from book.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn','title', 'author', 'published_year', 'publisher', 'image_url_l']