from django.urls import path
from authentication.views import register, login_user, logout_user, index, get_books, admin_registration, \
    logout_mobile, mobile_login, register_mobile

app_name = 'authentication'

urlpatterns = [
    path('mobile-login/', mobile_login, name='mobile_login'),
    path('register-mobile/', register_mobile, name='register_mobile'),
    path('logout-mobile/', logout_mobile, name='logout_mobile'),
    path('register/', register, name='register'),
    path('admin-registration/', admin_registration, name='admin_registration'),
    path('login/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('api/book/', get_books, name='get_books'),
    path('', index, name='index')
]