
from django.shortcuts import render
from book.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect
from review_book.forms import ReviewForm
from django.urls import reverse

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


def add_review_ajax(request):
    if request.method == 'POST':
        ulasan = request.POST.get("ulasan")
        user = request.user

        new_review_book = Book(ulasan=ulasan, user=user)
        new_review_book.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
    
# def show_create_review(request):
#     form = ProductForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return HttpResponseRedirect(reverse('review_book:add_review'))

#     context = {'form': form}
#     return render(request, "create_review.html", context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ReviewBook
from review_book.forms import ReviewForm

@login_required
def show_create_review(request, book_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Ambil buku yang akan diulas
            book = Book.objects.get(pk=book_id)

            # Simpan ulasan ke database
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()

            return redirect('review_book', book_id=book_id)  # Ganti 'book_detail' dengan nama view untuk detail buku

    else:
        form = ReviewForm()

    return render(request, 'review_book:add_review.html', {'form': form})

