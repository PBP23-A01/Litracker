from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from book.models import Book
from django.contrib.auth.decorators import login_required

    

@login_required
def upvote_book(request):
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
    return render(request, "upvote_book.html", context)
