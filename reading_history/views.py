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
    current_user = User.objects.get(pk=pk)
    reading_history = ReadingHistory.objects.filter(pk=pk)
    context = {
        'reading_history': reading_history,
        'user' : current_user
    }
    return render(request, "reading_history.html", context)

# @login_required
# def readBook_ajax(request, book_id):
#     if request.method == 'POST':
#         book = Book.objects.get(id=book_id)  
#         last_page = request.POST.get("last_page")

#         reading_history = ReadingHistory(user=request.user, book_title=book.title, book_author=book.author, last_page=last_page)
#         reading_history.save()

#         return HttpResponse(b"CREATED", status=201)
#     return HttpResponseNotFound()

@login_required
def get_read_books(request):
    read_books = ReadingHistory.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", read_books), 
                        content_type="application/json")

@login_required
def history_book(request):
    # Get the user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Get the user's reading history
    reading_history = ReadingHistory.objects.filter(user=user_profile.user)

    # Check if there is any reading history for the user
    last_page = 0  # Default value if no reading history is found
    if reading_history.exists():
        last_page = reading_history.latest('date_opened').last_page

    context = {
        'reading_history': reading_history,
        'last_page': last_page,
    }

    return render(request, 'reading_history.html', context)



from django.shortcuts import render
from review_book.models import ReviewBook
from book.models import Book  # Import model Book

def get_last_page(request, book_id):
    # Dapatkan objek buku berdasarkan ID
    book = Book.objects.get(id=book_id)
    
    # Dapatkan objek ReviewBook yang sesuai untuk buku dan pengguna yang sudah login
    review = ReviewBook.objects.filter(book=book, user=request.user).last()
    
    # Ambil nilai last_page dari objek review (atau sesuaikan dengan nama kolom yang sesuai)
    last_page = review.last_page if review else None
    
    return render(request, 'get_last_page.html', {'last_page': last_page})