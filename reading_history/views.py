import json
from django.shortcuts import render, redirect, get_object_or_404
from book.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from reading_history.models import ReadingHistory
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# @login_required
# def add_history(request, book_id):
#     book = Book.objects.get(pk=book_id)
#     user_profile = UserProfile.objects.get(user=request.user)
#     user_profile.history_books.add(book)
#     return redirect('book_detail', book_id=book_id)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Book, ReadingHistory
import json

@csrf_exempt
def edit_page_number(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        book_id = received_data.get('bookId')
        new_page_number = received_data.get('newPageNumber')

        try:
            history_entry = ReadingHistory.objects.get(book_id=book_id)
            history_entry.last_page = new_page_number
            history_entry.save()
            return JsonResponse({'message': 'Page number edited successfully'}, status=201)
        except ReadingHistory.DoesNotExist:
            return JsonResponse({'message': 'Book not found in history'}, status=404)

@login_required
@csrf_exempt
def delete_history_entry(request, history_id):
    try:
        history_entry = get_object_or_404(ReadingHistory, pk=history_id, user=request.user)
        history_entry.delete()

        return HttpResponse("History entry deleted successfully", status=200)
    except Exception as err:
        print(err)
        return HttpResponse(status=500)
    
@login_required
def history_book(request):
    # Get the user's profile
    print(request.user)
    try:
        if request.method == 'POST':
            received_data = json.loads(request.body)
            user = request.user
            history_book = Book.objects.get(pk=received_data["bookId"])
            new_history = ReadingHistory(user = user, book = history_book, last_page = received_data["lastPage"])
            new_history.save()

            return HttpResponse(b"CREATED", status=201)
    except Exception as err:
        print(err)
    return HttpResponseNotFound

@csrf_exempt
def fetch_history(request):
    readingHistory = ReadingHistory.objects.all()
    list_desc = []
    list_history_book = []

    for j in readingHistory:
        last_page = j.last_page
        var = { 'user_id': j.user.pk, 'book_id': j.pk, 'last_page': j.last_page, 'date_opened':j.date_opened.strftime('%Y-%m-%d %H:%M:%S') }
        list_history_book.append(var)
    return JsonResponse({'history': list_history_book})

@login_required(login_url='/login')
def show_history(request):
    readingHistory = ReadingHistory.objects.filter(user=request.user)
    list_desc = []
    list_history_book = []

    for j in readingHistory:
        last_page = j.last_page
        list_history_book.append(history_book)
    
    list_set_history_book = set(list_history_book)
    list_history_book = (list(list_set_history_book))
    
    if request.method == "POST":
        hasil_cari = request.POST['hasil-book']
        list_search_history_book = []
        for k in list_history_book:
            if hasil_cari.lower() in k.nama_history_book.lower():
                list_search_history_book.append(k)
        list_history_book = list_search_history_book

    for i in list_history_book:
        str = i.description
        str = str[0:100]
        list_desc.append(str)

    books_info = zip(list_history_book,list_desc)   
    banyak_history_book = len(list_history_book)

    context = {
        'books':books_info,
        'last_page':last_page
    }
    
    return render(request,'history_book.html',context)

# def reading_history(request, pk):
#     current_user = User.objects.get(pk=pk)
#     reading_history = ReadingHistory.objects.filter(pk=pk)
#     context = {
#         'reading_history': reading_history,
#         'user' : current_user
#     }
#     return render(request, "reading_history.html", context)

# # @login_required
# # def readBook_ajax(request, book_id):
# #     if request.method == 'POST':
# #         book = Book.objects.get(id=book_id)  
# #         last_page = request.POST.get("last_page")

# #         reading_history = ReadingHistory(user=request.user, book_title=book.title, book_author=book.author, last_page=last_page)
# #         reading_history.save()

# #         return HttpResponse(b"CREATED", status=201)
# #     return HttpResponseNotFound()

# @login_required
# def get_read_books(request):
#     read_books = ReadingHistory.objects.filter(user=request.user)
#     return HttpResponse(serializers.serialize("json", read_books), 
#                         content_type="application/json")

# @login_required
# def history_book(request):
#     # Get the user's profile
#     user_profile = UserProfile.objects.get(user=request.user)

#     # Get the user's reading history
#     reading_history = ReadingHistory.objects.filter(user=user_profile.user)

#     # Check if there is any reading history for the user
#     last_page = 0  # Default value if no reading history is found
#     if reading_history.exists():
#         last_page = reading_history.latest('date_opened').last_page

#     context = {
#         'reading_history': reading_history,
#         'last_page': last_page,
#     }

#     return render(request, 'reading_history.html', context)



# from django.shortcuts import render
# from review_book.models import ReviewBook
# from book.models import Book  # Import model Book

# def get_last_page(request, book_id):
#     # Dapatkan objek history_book berdasarkan ID
#     book = Book.objects.get(id=book_id)
    
#     # Dapatkan objek ReviewBook yang sesuai untuk history_book dan pengguna yang sudah login
#     review = ReviewBook.objects.filter(book=book, user=request.user).last()
    
#     # Ambil nilai last_page dari objek review (atau sesuaikan dengan nama kolom yang sesuai)
#     last_page = review.last_page if review else None
    
#     return render(request, 'get_last_page.html', {'last_page': last_page})