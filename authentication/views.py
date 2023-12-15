import json
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from book.models import Book
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.db.models import F
from authentication.models import UserProfile
from authentication.forms import AdminRegistrationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:login_user')  # Redirect to the login page after successful registration
    context = {'form': form}
    return render(request, 'register.html', context)

def admin_registration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = True  # Make the user a superuser (admin)
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.userprofile.is_admin = True
            user_profile.save()
            login(request, user)
            messages.success(request, 'Admin account has been successfully created!')
            return redirect('book:show_homepage')  # Redirect to the desired admin page
        else:
            messages.error(request, 'Admin registration failed. Please check the form.')
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin_registration.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile(user=user)
                user_profile.save()
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
        books = Book.objects.annotate(
            total_votes=F('votes__total_votes')
        ).order_by('-total_votes')

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

@csrf_exempt
def mobile_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "id": user.id,  # Untuk filtering item di Flutter app nya
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def admin_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active and user.is_superuser:
            login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "id": user.id,
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun bukan admin atau dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def logout_mobile(request):
    username = request.user.username

    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

    
@csrf_exempt
def register_mobile(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": False, "message": "Username already used."}, status=400)

    user = User.objects.create_user(username=username, password=password)
    user.save()

    return JsonResponse({"username": user.username, "status": True, "message": "Register successful!"}, status=201)