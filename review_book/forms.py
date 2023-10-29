from django.forms import ModelForm
from review_book.models import ReviewBook

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewBook
        fields = ["review_text"]