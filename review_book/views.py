from django.shortcuts import render
from book.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound

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
    


