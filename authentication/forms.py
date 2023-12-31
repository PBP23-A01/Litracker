from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Add more fields as needed

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User

class AdminRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']