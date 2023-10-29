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
    return render(request, "show_review.html", context)

def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from review_book.models import Review

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})

def add_review(request, book_id):
    if request.method == 'POST':
        user = request.user
        book = get_object_or_404(Book, pk=book_id)
        content = request.POST.get('content', '')

        if content:
            review = Review.objects.create(user=user, book=book, content=content)
            return JsonResponse({'status': 'success', 'review_id': review.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Content cannot be empty'})

def delete_review(request, review_id):
    if request.method == 'POST':
        user = request.user
        review = get_object_or_404(Review, pk=review_id)

        if review.user == user:
            review.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You cannot delete this review'})