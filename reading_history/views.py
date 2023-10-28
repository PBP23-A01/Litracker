from django.shortcuts import render, redirect, get_object_or_404
from book.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from reading_history.models import ReadingHistory
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def reading_history(request, pk):
    current_user = User.objects.get(user_id=pk)
    reading_history = ReadingHistory.objects.filter(user_id=pk)
    context = {
        'reading_history': reading_history,
        'user' : current_user
    }
    return render(request, "reading_history.html", context)

# def reading_history(request, book_id):
#     if request.method == 'POST':
#         book = Book.objects.get(id=book_id)  

#         reading_history = ReadingHistory(user=request.user, book_title=book.title, book_author=book.author, date_finished=None, progress=0)
#         reading_history.save()

#         return HttpResponse(b"CREATED", status=201)
#     return HttpResponseNotFound()
