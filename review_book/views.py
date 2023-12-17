from django.shortcuts import get_object_or_404, render
from authentication.models import UserProfile
from review_book.models import Review
from book.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
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
    
def create_review(request):
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review_book:add_review'))

    context = {'form': form}
    return render(request, "create_review.html", context)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone

def format_time_difference(timestamp):
    time_difference = timezone.now() - timestamp
    if time_difference.days > 0:
        return f"{time_difference.days} h yang lalu"
    elif time_difference.seconds >= 3600:
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)} j {int(minutes)} m {int(seconds)} d yang lalu"
    elif time_difference.seconds >= 60:
        minutes, seconds = divmod(time_difference.seconds, 60)
        return f"{int(minutes)} m {int(seconds)} d yang lalu"
    else:
        return f"{int(time_difference.seconds)} d yang lalu"
    

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

@login_required
def commenting(request, book_id):
    book_instance = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        komentar = request.POST.get('komentar')

        # Validasi rating, pastikan berada dalam rentang 1 hingga 5
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError('Rating should be between 1 and 5.')
        except ValueError:
            return HttpResponseBadRequest('Invalid rating.')

        if komentar:
            beri_komentar, created = Review.objects.get_or_create(
                user=user_profile,
                book=book_instance,
                defaults={'rating': rating, 'comment': komentar}
            )

            if not created:
                beri_komentar.rating = rating
                beri_komentar.comment = komentar
                beri_komentar.save()

            response_data = {
                'message': 'Review added successfully.',
                'created': True,
                'username': user_profile.user.username,
                'book': book_instance.title,
                'rating': beri_komentar.rating,
                'comment': beri_komentar.comment,
                'timestamp': format_time_difference(beri_komentar.timestamp),
            }
        else:
            return HttpResponseBadRequest('Invalid comment in the request.')
    else:
        return HttpResponseBadRequest('Invalid request method')

    return JsonResponse(response_data)

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Count, Max
from django.utils import timezone

@csrf_exempt
def get_book_reviews(request, book_id):
    if request.method == 'GET':
        # Retrieve the book and its reviews
        book = Book.objects.get(pk=book_id)
        reviews = Review.objects.filter(book=book)

        # Create a list of dictionaries for the JSON response
        reviews_list = []
        for review in reviews:
            reviews_list.append({
                'username': review.user.user.username,
                'comment': review.comment,
                'timestamp': format_time_difference(review.timestamp),
                'rating': review.rating,
            })

        return JsonResponse({'book_id': book.id, 'reviews': reviews_list})
    else:
        return HttpResponseBadRequest('Invalid request method')




from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Check if the user has already liked the review
        if not CommentLike.objects.filter(review=review, user=user_profile).exists():
            like_instance = CommentLike.objects.create(review=review, user=user_profile)

            response_data = {
                'message': 'Review liked successfully.',
                'review_id': review.id,
                'like_id': like_instance.id,
            }

            return JsonResponse(response_data)
        else:
            return HttpResponseBadRequest('You have already liked this review.')
    else:
        return HttpResponseBadRequest('Invalid request method')
   