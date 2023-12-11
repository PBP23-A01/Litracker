from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from sympy import Sum
from book.models import Book
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def favorite_book(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_book = user_profile.wishlist_books.all()
    context = {'favorite_book': favorite_book}
    return render(request, 'favorite_book.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from book.models import BookVotes, BookWishlist

@require_GET
@login_required
def get_total_wishlist(request):
    user_profile = UserProfile.objects.get(user=request.user)
    total_wishlist = user_profile.upvoted_books.aggregate(Sum('wishlist__total_wishlist'))['wishlist__total_wishlist__sum']
    return JsonResponse({'total_wishlist': total_wishlist})