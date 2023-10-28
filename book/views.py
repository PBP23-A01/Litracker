from django.shortcuts import render
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
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'homepage.html', context)
