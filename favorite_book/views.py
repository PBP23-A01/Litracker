from django.shortcuts import get_object_or_404, render, redirect
from sympy import Sum
from book.models import Book
from favorite_book.models import WishlistBook
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def toggle_wishlist_flutter(request, book_id):
    book_instance = get_object_or_404(Book, pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Check if the user has already voted for the book
        wishlist, created = WishlistBook.objects.get_or_create(user=user_profile, book=book_instance)

        

        if created:
            message = 'Wishlisted'
        else:
            # If the user has already voted, delete the vote (unvote)
            wishlist.delete()
            message = 'Unwishlisted'

        total_wishlists = WishlistBook.objects.filter(book=book_instance, user=user_profile).count()


        return JsonResponse({'message': message, 'total_wishlists': total_wishlists})
    else:
        return HttpResponseBadRequest('Invalid request method')
    
@csrf_exempt
def get_wishlisting_users(request, book_id):
    book_instance = get_object_or_404(Book, pk=book_id)

    if request.method == 'GET':
        wishlisting_users = WishlistBook.objects.filter(book=book_instance)

        user_list = [wishlist.user.user.username for wishlist in wishlisting_users]

        user_profile = UserProfile.objects.get(user=request.user)
        is_user_in_list_orWishlistThisBook = user_profile.user.username in user_list
        
        book_info = {
            'model': 'book.book',
            'pk': book_instance.id,
            'fields': {
                'isbn': book_instance.isbn,
                'title': book_instance.title,
                'author': book_instance.author,
                'published_year': book_instance.published_year,
                'publisher': book_instance.publisher, 
                'image_url_s': book_instance.image_url_s,
                'image_url_m': book_instance.image_url_m,
                'image_url_l': book_instance.image_url_l,
                # Add other relevant book information
            }
        }

        return JsonResponse({'upvoting_users': user_list, 'total_users_wishlist': wishlisting_users.count(), 'book': book_info, 'isWishlist': is_user_in_list_orWishlistThisBook})
    else:
        return HttpResponseBadRequest('Invalid request method')
    
    

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