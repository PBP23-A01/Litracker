from django.shortcuts import render

def upvote_book(request):

    return render(request, "upvote_book.html")

