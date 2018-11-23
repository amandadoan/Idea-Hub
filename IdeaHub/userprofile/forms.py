from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

# Custom creation form for MyUser
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MyUser
        fields = ("username", "first_name", "last_name", "email", "date_of_birth", "profile_pic")
