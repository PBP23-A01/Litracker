from django.forms import ModelForm
from book.models import Book
from reading_history.models import ReadingHistory
from django import forms 

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn','title', 'author', 'published_year', 'publisher', 'image_url_l']

class ReadingHistoryForm(forms.ModelForm):
    class Meta:
        model = ReadingHistory
        fields = ['last_page']