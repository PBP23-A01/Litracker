from django.shortcuts import render

# Create your views here.
def show_review(request):
    return render(request, "review_book.html")

# from django.shortcuts import render, redirect
# from .models import ReviewBook
# from .forms import ReviewForm  # Anda perlu membuat form untuk ulasan, saya akan menambahkan ini sebagai contoh

# def review_book_list(request):
#     reviews = ReviewBook.objects.all()
#     return render(request, 'review_book/review_book_list.html', {'reviews': reviews})

# def add_review(request, book_id):
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             user = request.user.userprofile  # Menggunakan UserProfile yang sudah login
#             book = Book.objects.get(id=book_id)

#             ReviewBook.objects.create(user=user, book=book, text=text)
#             return redirect('review_book_list')

#     else:
#         form = ReviewForm()

#     return render(request, 'review_book/add_review.html', {'form': form})

