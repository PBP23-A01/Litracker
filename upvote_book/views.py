import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from sympy import Sum
from upvote_book.models import MyUpvoteListFlutter, UpvotedbyUsersFlutter
from book.models import Book
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

    

# @login_required
# def upvote_book(request):
#     user = request.user
#     books = Book.objects.all().order_by('-total_votes')
    
#     context = {'books': books}
#     return render(request, "upvote_book.html", context)

@login_required
def add_upvote(request, book_id):
    book = Book.objects.get(pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.upvoted_books.add(book)
    return redirect('book_detail', book_id=book_id)

@login_required
def upvote_book(request):
    # Get the user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Get the books that the user has upvoted
    upvoted_books = user_profile.upvoted_books.all()

    context = {'upvoted_books': upvoted_books}

    # You can now pass 'upvoted_books' to your template to display the list
    return render(request, 'upvote_book.html', context)













def data_upvote_flutter(request, book_id):
    user_profile = UserProfile.objects.get(user=request.user)
    book = Book.objects.get(pk=book_id)

    data = json.loads(request.body)
    if request.method == "POST":

        # Membuat objek MyUpvoteList
        i_upvote, created_upvote = MyUpvoteListFlutter.objects.get_or_create(
            me=user_profile,
            books=book,
            reasoning=data["my_reason"]
        )

        # Memeriksa apakah user belum pernah upvote buku ini
        if created_upvote:
            i_upvote.save()

        # Membuat objek UpvotedbyUsers
        book_upvoted_by_users, created_book_upvote = UpvotedbyUsersFlutter.objects.get_or_create(
            book=book,
            users=user_profile,
        )

        # Memeriksa apakah user belum ada di daftar upvoter suatu buku
        if created_book_upvote:
            book_upvoted_by_users.save()

        return JsonResponse({"status": "success"}, status=200)
    
    else:
        return JsonResponse({"status": "error"}, status=401)
    

def display_upvote_users_flutter(request, book_id):
    
    data = json.loads(request.body)

    # Mendapatkan objek buku
    book = Book.objects.get(pk=book_id)

    # Mendapatkan semua objek UpvotedbyUsers yang terkait dengan buku tersebut
    upvoters = UpvotedbyUsersFlutter.objects.filter(book=book)

    if request.method == "GET":
    # Membuat daftar user dan komen masing-masing user yang upvote buku tersebut
        upvote_data = []
        for upvoter in upvoters:
            users = upvoter.users.all()
            comments = MyUpvoteListFlutter.objects.filter(me__in=users, books=book).values('me__user__username', 'reasoning')
            upvote_data.append({"users": list(users.values_list('user__username', flat=True)), "comments": list(comments)})

        return JsonResponse({"upvote_data": upvote_data}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)


def display_upvoted_books_flutter(request):
    data = json.loads(request.body)

    if request.method == "GET":
        # Mendapatkan objek user_profile
        user_profile = UserProfile.objects.get(user=request.user)

        # Mendapatkan semua buku yang diupvote oleh user tersebut
        upvoted_books = MyUpvoteListFlutter.objects.filter(me=user_profile).values('books__title', 'books__author')

        return JsonResponse({"upvoted_books": list(upvoted_books)}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)