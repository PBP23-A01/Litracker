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

        total_votes = Vote.objects.filter(book=book_instance).count()

        return JsonResponse({'message': message, 'total_votes': total_votes})
    else:
        return HttpResponseBadRequest('Invalid request method')
