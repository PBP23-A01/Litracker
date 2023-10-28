from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Add more fields as needed

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
