from django.urls import path
from authentication.views import register, login_user

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
]