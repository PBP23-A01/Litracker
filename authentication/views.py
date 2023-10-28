from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from book.models import Book
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers

# Create your views here.

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login_user')  # Redirect to the login page after successful registration
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a different URL or page after successful login (not 'authentication:login')
            return redirect('book:show_homepage')  # Change 'some_other_page' to the URL you want to redirect to
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('authentication:index')  # Redirect to the login page after logout

def index(request):
    if request.user.is_authenticated:
        return redirect('book:show_homepage')  # Redirect to the book:index view
    else:
        books = Book.objects.all().order_by('-total_votes')

        rank = 0
        prev_votes = None
        
        for book in books:
            if book.total_votes != prev_votes:
                rank += 1
            book.rank = rank
            prev_votes = book.total_votes
        
        context = {'books': books}
        return render(request,'index.html', context)

def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
                        content_type="application/json")