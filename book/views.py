import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from book.models import Book
from book.forms import BookForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
                        content_type="application/json")

def show_homepage(request):
    books = Book.objects.all()
    context = {'books': books}
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
def find_book(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        title = data.get("title", "")
        author = data.get("author", "")
        publisher = data.get("publisher", "")
        published_year = data.get("published_year", "")

        # Construct a filter based on the provided parameters
        filters = {}
        
        if title:
            filters['title__icontains'] = title
        if author:
            filters['author__icontains'] = author
        if publisher:
            filters['publisher__icontains'] = publisher
        if published_year:
            filters['published_year__icontains'] = published_year

        # Apply the filters to the Book queryset
        books = Book.objects.filter(**filters).values()

        return JsonResponse({'books': list(books)}, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)