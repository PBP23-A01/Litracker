from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from book.models import Book
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

@login_required
def upvote_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    book.total_votes += 1
    book.save()
    return redirect('authentication:index')
