import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db import transaction
from django.db.models import Q
from book.models import Book
from authentication.models import UserProfile
from book.forms import BookForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from reading_history.models import ReadingHistory
from .forms import ReadingHistoryForm

# Create your views here.
def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
                        content_type="application/json")

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
    if request.user.is_authenticated:
        try:
            context['last_login'] = request.COOKIES['last_login']
        except KeyError:
            context['last_login'] = 'None'
    return render(request, 'homepage.html', context)


def is_admin(user):
    return user.userprofile.is_admin

@login_required
@user_passes_test(is_admin)
def tambah_buku(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = BookForm()
    return render(request, 'tambah_buku.html', {'form': form})

@csrf_exempt
def search_books(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "")

        if title:
            # Use Q objects to perform a case-insensitive search on both title and author
            results = Book.objects.filter(Q(title__icontains=title) | Q(author__icontains=title)).values()
        else:
            results = []

    else:
        results = Book.objects.all().values()

    return JsonResponse({'books': list(results)})
    
# @login_required
# def upvote_book(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)

#     book.total_votes += 1
#     book.save()
#     return redirect('authentication:index')

@login_required
def upvote_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if book in user_profile.upvoted_books.all():
        # User has already upvoted the book, so remove the upvote
        user_profile.upvoted_books.remove(book)
        book.total_votes -= 1
    else:
        # User has not upvoted the book, so add the upvote
        user_profile.upvoted_books.add(book)
        book.total_votes += 1

    # Save the changes to both the book and user profile within a transaction
    with transaction.atomic():
        user_profile.save()
        book.save()

    # Return a JSON response indicating success or failure
    return redirect('authentication:index')

@login_required
def wishlist_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if book in user_profile.wishlist_books.all():
        user_profile.wishlist_books.remove(book)
        book.total_wishlist -= 1
    else:
        user_profile.wishlist_books.add(book)
        book.total_wishlist += 1

    with transaction.atomic():
        user_profile.save()
        book.save()

    return redirect('authentication:index')

@login_required
def last_page(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if book in user_profile.history_books.all():
        # User has already upvoted the book, so remove the upvote
        user_profile.history_books.remove(book)
        book.progress = 0
    else:
        # User has not upvoted the book, so add the upvote
        user_profile.history_books.add(book)
        book.progress = last_page

    # Save the changes to both the book and user profile within a transaction
    with transaction.atomic():
        user_profile.save()
        book.save()

    # Return a JSON response indicating success or failure
    return redirect('authentication:index')

def simpan_last_page(request, book_id):
    # Ambil objek ReadingHistory yang sesuai dengan user dan buku
    user = request.user
    book = Book.objects.get(id=book_id)
    reading_history, created = ReadingHistory.objects.get_or_create(user=user, book=book)

    # Ambil nilai last_page dari permintaan POST
    last_page = request.POST.get('last_page')

    if last_page is not None:
        # Simpan nilai last_page ke dalam objek ReadingHistory
        reading_history.last_page = last_page
        reading_history.save()

        # Berikan respons JSON yang sesuai
        response_data = {
            'message': 'Last page saved successfully.'
        }

        return JsonResponse(response_data)
    else:
        # Jika tidak ada nilai last_page yang diberikan, berikan respons JSON dengan pesan kesalahan
        response_data = {
            'error': 'Last page is required.'
        }

        return JsonResponse(response_data, status=400)



# @login_required
# def add_upvote(request, book_id):
#     book = Book.objects.get(pk=book_id)
#     user_profile = UserProfile.objects.get(user=request.user)

#     if book in user_profile.upvoted_books.all():
#         # User has already upvoted the book, so remove the upvote
#         user_profile.upvoted_books.remove(book)
#     else:
#         # User has not upvoted the book, so add the upvote
#         user_profile.upvoted_books.add(book)

#     return redirect('authentication:index', book_id=book_id)