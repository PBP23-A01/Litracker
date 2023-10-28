from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from book.models import Book
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
                        content_type="application/json")

@login_required
def show_homepage(request):
    user = request.user
    books = Book.objects.all().order_by('-total_votes')

    rank = 0
    prev_votes = None
    
    for book in books:
        if book.total_votes != prev_votes:
            rank += 1
        book.rank = rank
        prev_votes = book.total_votes
    
    context = {'books': books}
    return render(request, 'homepage.html', context)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# @login_required
# def upvote_book(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)

#     book.total_votes += 1
#     book.save()
#     return redirect('authentication:index')


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction

@login_required
def upvote_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if book in user_profile.books.all():
        # User has already upvoted the book, so remove the upvote
        user_profile.books.remove(book)
        book.total_votes -= 1
    else:
        # User has not upvoted the book, so add the upvote
        user_profile.books.add(book)
        book.total_votes += 1

    # Save the changes to both the book and user profile within a transaction
    with transaction.atomic():
        user_profile.save()
        book.save()

    # Return a JSON response indicating success or failure
    return redirect('authentication:index')


# @login_required
# def add_upvote(request, book_id):
#     book = Book.objects.get(pk=book_id)
#     user_profile = UserProfile.objects.get(user=request.user)

#     if book in user_profile.upvoted_books.all():
#         # User has already upvoted the book, so remove the upvote
#         user_profile.upvoted_books.remove(book)
#     else:
#         # User has not upvoted the book, so add the upvote
#         user_profile.upvoted_books.add(book)

#     return redirect('authentication:index', book_id=book_id)