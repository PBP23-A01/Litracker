import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.core import serializers
from sympy import Sum
from upvote_book.models import Upvote, Vote
from book.models import Book
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

    

# @login_required
# def upvote_book(request):
#     user = request.user
#     books = Book.objects.all().order_by('-total_votes')
    
#     context = {'books': books}
#     return render(request, "upvote_book.html", context)

@login_required
def add_upvote(request, book_id):
    book = Book.objects.get(pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.upvoted_books.add(book)
    return redirect('book_detail', book_id=book_id)

@login_required
def upvote_book(request):
    # Get the user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Get the books that the user has upvoted
    upvoted_books = user_profile.upvoted_books.all()

    context = {'upvoted_books': upvoted_books}

    # You can now pass 'upvoted_books' to your template to display the list
    return render(request, 'upvote_book.html', context)






from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404



# Cek peringkat buku-buku dengan melihat total votes. Jika ada jumlah votes sama, maka buku dengan upvote terbaru memiliki peringkat lebih tinggi.
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Max

@csrf_exempt
def get_top_books(request):
    if request.method == 'GET':
        # Retrieve all books with their total upvotes and latest upvote timestamp
        books = Book.objects.annotate(
            total_upvotes=Count('vote'),
            latest_upvote=Max('vote__created_at')
        ).order_by('-total_upvotes', '-latest_upvote')[:10]

        # Create a list of dictionaries for the JSON response
        top_books_list = []
        for book in books:
            top_books_list.append({
                'book_id': book.id,
                'title': book.title,
                'author': book.author,  # Add the author information
                'total_upvotes': book.total_upvotes,
                'image_url_l': book.image_url_l,
                'image_url_m': book.image_url_m,
                'image_url_s': book.image_url_s,
                'latest_upvote_time': format_time_difference(book.latest_upvote),
            })

        return JsonResponse({'top_books': top_books_list})
    else:
        return HttpResponseBadRequest('Invalid request method')

def format_time_difference(timestamp):
    if timestamp is None:
        return "Tidak ada data upvote terakhir"  # or any default value you prefer for cases where the timestamp is None

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


    
# Hak upvote dan batal upvote user
@csrf_exempt
def toggle_upvote_flutter(request, book_id):
    book_instance = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Check if the user has already voted for the book
        vote, created = Vote.objects.get_or_create(user=user_profile, book=book_instance)

        

        if created:
            message = 'Upvoted'
        else:
            # If the user has already voted, delete the vote (unvote)
            vote.delete()
            message = 'Unvoted'

        total_votes = Vote.objects.filter(book=book_instance, user=user_profile).count()


        return JsonResponse({'message': message, 'total_votes': total_votes})
    else:
        return HttpResponseBadRequest('Invalid request method')


# Siapa saja user yang upvote buku X dan berapa user yang upvote buku X?
# Serta cek apakah user Y sudah upvote buku X
@csrf_exempt
def get_upvoting_users(request, book_id):
    book_instance = get_object_or_404(Book, pk=book_id)

    if request.method == 'GET':
        # Retrieve the list of users who upvoted the book
        upvoting_users = Vote.objects.filter(book=book_instance)

        # Convert the QuerySet to a list of dictionaries
        user_list = [vote.user.user.username for vote in upvoting_users]

        # Check if a specific user is in the user_list
        user_profile = UserProfile.objects.get(user=request.user)
        is_user_in_list_orUpvoteThisBook = user_profile.user.username in user_list
        
        # Include book information in the JSON response
        book_info = {
            'model': 'book.book',
            'pk': book_instance.id,
            'fields': {
                'isbn': book_instance.isbn,
                'title': book_instance.title,
                'author': book_instance.author,
                'published_year': book_instance.published_year,
                'publisher': book_instance.publisher,  # Add the publisher field if available
                'image_url_s': book_instance.image_url_s,
                'image_url_m': book_instance.image_url_m,
                'image_url_l': book_instance.image_url_l,
                # Add other relevant book information
            }
        }

        return JsonResponse({'upvoting_users': user_list, 'total_users_upvote': upvoting_users.count(), 'book': book_info, 'isUpvote': is_user_in_list_orUpvoteThisBook})
    else:
        return HttpResponseBadRequest('Invalid request method')
    

# Buku apa saja yang user upvote berapa jumlah buku yang telah user upvote?
@csrf_exempt
def get_upvoted_books(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'GET':
        upvoted_books = Vote.objects.filter(user=user_profile)
        books_list = []
        for vote in upvoted_books:
            book_instance = vote.book
            book_info = {
                'model': 'book.book',
                'pk': book_instance.id,
                'fields': {
                    'isbn': book_instance.isbn,
                    'title': book_instance.title,
                    'author': book_instance.author,
                    'published_year': book_instance.published_year,
                    'publisher': book_instance.publisher,  # Add the publisher field if available
                    'image_url_s': book_instance.image_url_s,
                    'image_url_m': book_instance.image_url_m,
                    'image_url_l': book_instance.image_url_l,
                    # Add other relevant book information
                }
            }
            books_list.append(book_info)
            
        total_upvoted_books = len(upvoted_books)

        return JsonResponse({'total_upvoted_books': total_upvoted_books, 'upvoted_books': books_list, }, json_dumps_params={'indent': 2})
        # return JsonResponse({'total_upvoted_books':total_upvoted_books},safe=False)
    else:
        return HttpResponseBadRequest('Invalid request method')
