
from django.shortcuts import render
from book.models import Book
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
def show_review(request):
    books =Book.objects.all()
    context = {
        'books': books
    }
    return render(request, "review_book.html", context)

def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def add_review(request):
    return render(request, 'add_review.html')



# from django.shortcuts import render, redirect
# from .models import ReviewBook
# from .forms import ReviewForm  # Anda perlu membuat form untuk ulasan, saya akan menambahkan ini sebagai contoh

# def review_book_list(request):
#     reviews = ReviewBook.objects.all()
#     return render(request, 'review_book/review_book_list.html', {'reviews': reviews})

# def add_review(request, book_id):
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             user = request.user.userprofile  # Menggunakan UserProfile yang sudah login
#             book = Book.objects.get(id=book_id)

#             ReviewBook.objects.create(user=user, book=book, text=text)
#             return redirect('review_book_list')

#     else:
#         form = ReviewForm()

#     return render(request, 'review_book/add_review.html', {'form': form})

