from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from book.models import Book
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

    

@login_required
def favorite_book(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_book = user_profile.wishlist_books.all()
    context = {'favorite_book': favorite_book}
    return render(request, 'favorite_book.html', context)