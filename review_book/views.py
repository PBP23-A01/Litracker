from django.shortcuts import get_object_or_404, render
from authentication.models import UserProfile
from review_book.models import Review
from book.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.http import HttpResponseRedirect
from review_book.forms import ReviewForm
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Max
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

def format_time_differences(timestamp):
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

def get_all_reviews(request):
    if request.method == 'GET':
        # Retrieve all reviews
        reviews = Review.objects.all()

        # Create a list of dictionaries for the JSON response
        reviews_list = []
        for review in reviews:
            reviews_list.append({
                'id': review.id,
                'book_id': review.book.id,
                'username': review.user.user.username,
                'comment': review.comment,
                'rating': review.rating,
                'timestamp': review.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                # Format the timestamp as you prefer
            })

        return JsonResponse({'reviews': reviews_list})
    else:
        return HttpResponseBadRequest('Invalid request method')

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
                'id': review.id,  # Include the review's ID
                'username': review.user.user.username,
                'comment': review.comment,
                'timestamp': format_time_differences(review.timestamp),
                'rating': review.rating,
            })

        # Get the count of reviews
        reviews_count = len(reviews_list)

        return JsonResponse({'book_id': book.id, 'reviews': reviews_list, 'reviews_count': reviews_count})
    else:
        return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def post_book_review(request, book_id):
    if request.method == 'POST':
        # Extract the data from the request
        username = request.POST.get('username')
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # Validate and sanitize the data
        if not all([username, comment, rating]):
            return HttpResponseBadRequest('Missing required fields')

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return HttpResponseBadRequest('Invalid rating value')
        except ValueError:
            return HttpResponseBadRequest('Invalid rating value')

        # Retrieve the book and user
        try:
            book = Book.objects.get(pk=book_id)
            user = UserProfile.objects.get(user__username=username)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Invalid book ID or username')

        # Create the review
        review = Review(book=book, user=user, comment=comment, rating=rating, timestamp=timezone.now())
        review.save()

        return JsonResponse({'message': 'Review created successfully'}, status=200)
    else:
        return HttpResponseBadRequest('Invalid request method')


@csrf_exempt
def delete_book_review(request, review_id):
    if request.method == 'DELETE':
        # Retrieve the review
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return HttpResponseBadRequest('Invalid review ID')

        # Delete the review
        review.delete()

        reviews_count = Review.objects.all().count()

        return JsonResponse({'message': 'Review deleted successfully', 'reviews_count': reviews_count}, status=200)
    else:
        return HttpResponseBadRequest('Invalid request method')

# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse, HttpResponseBadRequest
# from django.contrib.auth.decorators import login_required

# @login_required
# def like_review(request, review_id):
#     review = get_object_or_404(Review, pk=review_id)
#     user_profile = UserProfile.objects.get(user=request.user)

#     if request.method == 'POST':
#         # Check if the user has already liked the review
#         if not CommentLike.objects.filter(review=review, user=user_profile).exists():
#             like_instance = CommentLike.objects.create(review=review, user=user_profile)

#             response_data = {
#                 'message': 'Review liked successfully.',
#                 'review_id': review.id,
#                 'like_id': like_instance.id,
#             }

#             return JsonResponse(response_data)
#         else:
#             return HttpResponseBadRequest('You have already liked this review.')
#     else:
#         return HttpResponseBadRequest('Invalid request method')


from django.db.models import Avg, IntegerField
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone

from django.utils import timezone
from datetime import datetime

def format_time_difference(timestamp):
    if timestamp is None:
        return "Tidak ada data upvote terakhir"  # or any default value you prefer for cases where the timestamp is None

    if not isinstance(timestamp, datetime):
        # Parse the timestamp string into a datetime object
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    # Make the timestamp aware
    timestamp = timezone.make_aware(timestamp)

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
    

from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Avg, IntegerField
from django.db.models.functions import Coalesce
from django.utils import timezone

def get_snippet_reviews_without_rating(request):
    if request.method == 'GET':
        # Retrieve all reviews
        reviews = Review.objects.all()

        # Create a dictionary to store reviews for each book
        book_reviews = {}

        # Aggregate reviews for each book
        for review in reviews:
            book_id = review.book.id
            if book_id not in book_reviews:
                book_reviews[book_id] = {
                    'id': book_id,
                    'title': review.book.title,
                    'author': review.book.author,
                    'image': review.book.image_url_l,
                    'reviews': [],
                }

            # Append review details to the book's reviews list
            book_reviews[book_id]['reviews'].append({
                'id': review.id,
                'username': review.user.user.username,
                'comment': review.comment,
                'timestamp': review.timestamp,  # Use the datetime object directly
            })

        # Process the aggregated reviews for each book
        final_reviews_list = []
        for book_id, book_data in book_reviews.items():
            # Limit the number of reviews to 3
            book_data['reviews'] = book_data['reviews'][:3]

            # Get the latest timestamp among the three most recent reviews
            latest_timestamp = max(book_data['reviews'], key=lambda r: r['timestamp'])['timestamp']

            # Format the latest timestamp as a string
            latest_timestamp_str = latest_timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Add the formatted timestamp to the book's data
            book_data['formatted_timestamp'] = format_time_difference(latest_timestamp_str)

            final_reviews_list.append(book_data)

        # Sort the final reviews list based on the latest timestamp in each book's reviews
        final_reviews_list.sort(key=lambda x: max(x['reviews'], key=lambda r: r['timestamp'])['timestamp'], reverse=True)

        return JsonResponse({'reviews': final_reviews_list})
    else:
        return HttpResponseBadRequest('Invalid request method')

def get_snippet_reviews_without_timestamp(request):
    if request.method == 'GET':
        # Retrieve all reviews
        reviews = Review.objects.all()

        # Create a dictionary to store reviews for each book
        book_reviews = {}

        # Aggregate reviews for each book
        for review in reviews:
            book_id = review.book.id
            if book_id not in book_reviews:
                book_reviews[book_id] = {
                    'id': book_id,
                    'title': review.book.title,  # Assuming Book model has a 'title' field
                    'author': review.book.author,
                    'image': review.book.image_url_l,
                    'reviews': [],
                }

            # Append review details to the book's reviews list
            book_reviews[book_id]['reviews'].append({
                'id': review.id,
                'username': review.user.user.username,
                'comment': review.comment,
                'rating': review.rating,
            })

        # Process the aggregated reviews for each book
        final_reviews_list = []
        for book_id, book_data in book_reviews.items():
            # Limit the number of reviews to 3
            book_data['reviews'] = book_data['reviews'][:3]

            # Calculate the average rating for the book
            avg_rating = Review.objects.filter(book_id=book_id).aggregate(avg_rating=Coalesce(Avg('rating'), 0, output_field=IntegerField()))['avg_rating']

            # Add average rating to the book's data
            book_data['average_rating'] = avg_rating

            final_reviews_list.append(book_data)

        # Sort the final reviews list based on the latest timestamp in each book's reviews
            final_reviews_list.sort(key=lambda x: x['average_rating'], reverse=True)


        return JsonResponse({'reviews': final_reviews_list})
    else:
        return HttpResponseBadRequest('Invalid request method')
