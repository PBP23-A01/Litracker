from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from book.models import Book
from review.models import Review
from django.core import serializers
from django.contrib.auth.models import User
from authentication.models import UserProfile

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

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from book.models import Book
from review.models import Review
from django.core import serializers

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book)
    
    allreviews = Review.objects.all()
    user = request.user  # Add this line to get the user
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews, 'allreviews': allreviews, 'user': user})


from authentication.models import UserProfile  # Pastikan Anda mengimpor model UserProfile yang benar

def add_review(request, book_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'You must be logged in to add a review'})

        user_profile = UserProfile.objects.get(user=request.user)  # Menggunakan UserProfile untuk mendapatkan pengguna
        book = get_object_or_404(Book, pk=book_id)
        content = request.POST.get('content', '')

        if content:
            review = Review.objects.create(user=user_profile, book=book, content=content)  # Menggunakan user_profile
            return JsonResponse({'status': 'success', 'review_id': review.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Content cannot be empty'})
    else:
        return HttpResponseForbidden()


from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Review  # Import your Review model here

def delete_review(request, review_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'You must be logged in to delete a review'})

        try:
            review_id = int(review_id)  # Ensure it's a valid integer
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid review ID'})

        try:
            review = get_object_or_404(Review, pk=review_id)
        except Review.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Review not found'})

        if review.user == request.user:
            review.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You cannot delete this review'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
