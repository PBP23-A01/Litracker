from django.shortcuts import render, redirect
from sympy import Sum
from favorite_book.models import WishlistBook
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@login_required
def favorite_book(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_book = user_profile.wishlist_books.all()
    context = {'favorite_book': favorite_book}
    return render(request, 'favorite_book.html', context)

@require_GET
@login_required
def get_total_wishlist(request):
    user_profile = UserProfile.objects.get(user=request.user)
    total_wishlist = user_profile.upvoted_books.aggregate(Sum('wishlist__total_wishlist'))['wishlist__total_wishlist__sum']
    return JsonResponse({'total_wishlist': total_wishlist})




from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required  # Use the login_required decorator to ensure the user is authenticated
def get_wishlisted_books(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('User is not authenticated')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseBadRequest('UserProfile not found for the authenticated user')

    if request.method == 'GET':
        wishlisted_books = WishlistBook.objects.filter(user=user_profile)
        books_list = []
        for wishlist in wishlisted_books:
            book_instance = wishlist.book
            upvoting_users = WishlistBook.objects.filter(book=book_instance)
            book_info = {
                'id': book_instance.id,
                'isbn': book_instance.isbn,
                'title': book_instance.title,
                'author': book_instance.author,
                'published_year': book_instance.published_year,
                'publisher': book_instance.publisher,
                'image_url_s': book_instance.image_url_s,
                'image_url_m': book_instance.image_url_m,
                'image_url_l': book_instance.image_url_l,
                'total_wishlist_thisbook': upvoting_users.count()
            }
            books_list.append(book_info)

        total_wishlisted_books = len(wishlisted_books)

        return JsonResponse({'total_wishlisted_books': total_wishlisted_books, 'wishlisted_books': books_list}, json_dumps_params={'indent': 2})
    else:
        return HttpResponseBadRequest('Invalid request method')