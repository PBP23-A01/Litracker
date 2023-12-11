from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from sympy import Sum
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


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from book.models import BookVotes, BookWishlist

@require_GET
@login_required
def get_total_votes(request):
    user_profile = UserProfile.objects.get(user=request.user)
    total_votes = user_profile.upvoted_books.aggregate(Sum('votes__total_votes'))['votes__total_votes__sum']
    return JsonResponse({'total_votes': total_votes})