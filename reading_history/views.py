import json
from django.shortcuts import render, redirect, get_object_or_404
from book.models import Book
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from reading_history.models import ReadingHistory
from authentication.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
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

# GET semua reading history dari semua buku, bisa untuk liat data JSON di web
def get_all_reading_histories(request):
    if request.method == 'GET':
        # Retrieve all reading histories
        reading_histories = ReadingHistory.objects.all()

        # Create a list of dictionaries for the JSON response
        reading_histories_list = []
        for history in reading_histories:
            reading_histories_list.append({
                'id': history.id,
                'book_id': history.book.pk,
                'username': history.user.user.username,
                'last_page': history.last_page,
                'date_opened': history.date_opened.strftime('%Y-%m-%d'),
            })

        return JsonResponse({'reading_histories': reading_histories_list})
    else:
        return HttpResponseBadRequest('Invalid request method')

# GET reading history dari buku buat nanti di filternya di flutter
@csrf_exempt
def get_reading_history(request, book_id):
    if request.method == 'GET':
        # Retrieve the book and its reading history
        book = Book.objects.get(pk=book_id)
        reading_histories = ReadingHistory.objects.filter(book=book)

        # Create a list of dictionaries for the JSON response
        reading_histories_list = []
        for history in reading_histories:
            reading_histories_list.append({
                'id': history.id,
                'username': history.user.user.username,
                'last_page': history.last_page,
                'date_opened': history.date_opened.strftime('%Y-%m-%d'),
            })

        return JsonResponse({'book_id': book.id, 'reading_histories': reading_histories_list})
    else:
        return HttpResponseBadRequest('Invalid request method')

# View POST sekaligus untuk edit
@csrf_exempt
def post_reading_history(request, book_id):
    if request.method == 'POST':
        # Extract data from the request
        username = request.POST.get('username')
        last_page = request.POST.get('last_page')

        # Validate the data
        if not last_page:
            return HttpResponseBadRequest('Missing required fields')

        try:
            last_page = int(last_page)
            if last_page < 0:
                return HttpResponseBadRequest('Invalid last page value')
        except ValueError:
            return HttpResponseBadRequest('Invalid last page value')

        # Retrieve the book and user
        try:
            book = Book.objects.get(pk=book_id)
            user = UserProfile.objects.get(user__username=username)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Invalid book ID or username')

        # Check if a reading history already exists for this book and user
        try:
            reading_history = ReadingHistory.objects.get(book=book, user=user)
            # If it does, update the last_page field
            reading_history.last_page = last_page
            reading_history.save()
            message = 'Reading history updated successfully'
        except ReadingHistory.DoesNotExist:
            # If it doesn't, create a new reading history
            reading_history = ReadingHistory(book=book, user=user, last_page=last_page)
            reading_history.save()
            message = 'Reading history created successfully'

        return JsonResponse({'message': message}, status=200)
    else:
        return HttpResponseBadRequest('Invalid request method')
    
# View DELETE untuk delete data yang tersimpan di JSON pada flutter
@csrf_exempt
def delete_reading_history(request, history_id):
    if request.method == 'DELETE':
        # Retrieve the reading history
        try:
            reading_history = ReadingHistory.objects.get(pk=history_id)
        except ReadingHistory.DoesNotExist:
            return HttpResponseBadRequest('Invalid history ID')

        # Delete the reading history
        reading_history.delete()

        return JsonResponse({'message': 'Reading history deleted successfully'})
    else:
        return HttpResponseBadRequest('Invalid request method')

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