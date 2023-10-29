from django.shortcuts import render, redirect
from book.models import Book
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def add_favorite(request, book_id):
    book = Book.objects.get(pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.wishlist_books.add(book)
    return redirect('book_detail', book_id=book_id)

@login_required
def show_favorite(request):
    # Get the user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Get the books that the user has upvoted
    wishlist_books = user_profile.wishlist_books.all()

    context = {'wishlist_books': wishlist_books}

    # You can now pass 'upvoted_books' to your template to display the list
    return render(request, 'favorite.html', context)