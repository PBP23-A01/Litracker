import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db import transaction
from django.db.models import Q
from book.models import Book, BookVotes, BookWishlist
from authentication.models import UserProfile
from book.forms import BookForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
                        content_type="application/json")


@login_required
def upvote_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    book_vote, created = BookVotes.objects.get_or_create(book=book)

    if book in user_profile.upvoted_books.all():
        user_profile.upvoted_books.remove(book)
        book_vote.total_votes -= 1
    else:
        user_profile.upvoted_books.add(book)
        book_vote.total_votes += 1

    with transaction.atomic():
        user_profile.save()
        book_vote.save()

    return redirect('authentication:index')

@login_required
def wishlist_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    book_wishlist, created = BookWishlist.objects.get_or_create(book=book)

    if book in user_profile.wishlist_books.all():
        user_profile.wishlist_books.remove(book)
        book_wishlist.total_wishlist -= 1
    else:
        user_profile.wishlist_books.add(book)
        book_wishlist.total_wishlist += 1

    with transaction.atomic():
        user_profile.save()
        book_wishlist.save()

    return redirect('authentication:index')

@login_required
def upvote_book_mobile(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    book_vote, created = BookVotes.objects.get_or_create(book=book)

    if book in user_profile.upvoted_books.all():
        user_profile.upvoted_books.remove(book)
        book_vote.total_votes -= 1
    else:
        user_profile.upvoted_books.add(book)
        book_vote.total_votes += 1

    with transaction.atomic():
        user_profile.save()
        book_vote.save()

    total_votes = book.upvoters.count()
    return JsonResponse({'total_votes': total_votes})

@login_required
def wishlist_book_mobile(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    book_wishlist, created = BookWishlist.objects.get_or_create(book=book)

    if book in user_profile.wishlist_books.all():
        user_profile.wishlist_books.remove(book)
        book_wishlist.total_wishlist -= 1
    else:
        user_profile.wishlist_books.add(book)
        book_wishlist.total_wishlist += 1

    with transaction.atomic():
        user_profile.save()
        book_wishlist.save()

    total_wishlist = book.wishlists.count()
    return JsonResponse({'total_wishlist': total_wishlist})

def show_homepage(request):
    user = request.user
    books = Book.objects.all()

    rank = 0
    prev_votes = None
    
    for book in books:
        book_vote, created = BookVotes.objects.get_or_create(book=book)
        if book_vote.total_votes != prev_votes:
            rank += 1
        book.rank = rank
        prev_votes = book_vote.total_votes

    context = {'books': books}
    if request.user.is_authenticated:
        try:
            context['last_login'] = request.COOKIES['last_login']
        except KeyError:
            context['last_login'] = 'None'
    return render(request, 'homepage.html', context)

def is_admin(user):
    return user.userprofile.is_admin

# Tambah buku untuk flutter
@csrf_exempt
def add_book_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        new_book = Book.objects.create(
            isbn = data["isbn"],
            title = data["title"],
            author = data["author"],
            published_year = int(data["published_year"]),
            publisher = data["publisher"],
            image_url_s = data["image_url_s"],
            image_url_m = data["image_url_m"],
            image_url_l = data["image_url_l"],
        )

        new_book.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_book_mobile(request, pk):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            book = Book.objects.get(pk=pk)
            print(book)
            for key, value in data.items():
                setattr(book, key, value)
            book.save()
            return JsonResponse({"status": "success"}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({"status": "error", "error": "Book not found"}, status=404)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_book_mobile(request, pk):
    if request.method == 'DELETE':
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({"status": "error", "error": "Book not found"}, status=404)
    else:
        return JsonResponse({"status": "error"}, status=401)

# Tambah buku untuk web app
def tambah_buku(request):
    try:
        # Ambil data dari permintaan POST
        data = json.loads(request.body.decode('utf-8'))

        # Buat instance BookForm dengan data dari permintaan
        form = BookForm(data)

        # Periksa validitas formulir
        if form.is_valid():
            # Simpan buku ke database
            form.save()

            # Berikan respons JSON yang sesuai
            response_data = {'message': 'Book added successfully'}
            return JsonResponse(response_data, status=201)

        else:
            # Jika formulir tidak valid, kirim pesan kesalahan JSON
            errors = form.errors.as_json()
            return JsonResponse({'error': errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
def search_books(request):
    search_term = request.GET.get('query', '')  # Mendapatkan kata kunci pencarian atau string kosong jika tidak ada

    results = []
    if search_term:
        results = Book.objects.filter(
            Q(title__icontains=search_term)    | # Cari judul yang mengandung search_term
            Q(author__icontains=search_term)   | # Cari penulis yang mengandung search_term
            Q(publisher__icontains=search_term)| # Cari penerbit yang mengandung search_term
            Q(published_year__icontains=search_term)
        )
    else:
        # Jika query kosong kembali ke homepage
        return redirect('book:show_homepage')
    return render(request, 'homepage.html', {'search_term': search_term, 'results': results})

@login_required
def history_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if book in user_profile.history_books.all():
        # User has already upvoted the book, so remove the upvote
        user_profile.history_books.remove(book)
    else:
        # User has not upvoted the book, so add the upvote
        user_profile.history_books.add(book)

    # Save the changes to both the book and user profile within a transaction
    with transaction.atomic():
        user_profile.save()
        book.save()

    # Return a JSON response indicating success or failure
    return redirect('authentication:index')


# @login_required
# def history_book(request, book_id):
#     if request.method == 'POST':
#         last_page.count = request.POST.get('last_page')

def render_form(request):
    return redirect('book:show_homepage')