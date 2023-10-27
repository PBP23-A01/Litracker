from django.shortcuts import render, redirect, get_object_or_404
from book.models import Book
from django.core import serializers
from django.http import HttpResponse
from reading_history.models import ReadingHistory
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required
def show_history(request, id):
    reading_history = ReadingHistory.objects.filter(pk=id, user=request.user)
    context = {
        'reading_history': reading_history
    }
    return render(request, "reading_history.html", context)

@login_required
def save_reading_history(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)  

        # Anda kemudian dapat membuat entri baru dalam riwayat bacaan pengguna
        reading_history = ReadingHistory(user=request.user, book_title=book.title, book_author=book.author, date_finished=None, progress=0)
        reading_history.save()

        return JsonResponse({'status': 'saved'})
    return JsonResponse({'status': 'error'})
