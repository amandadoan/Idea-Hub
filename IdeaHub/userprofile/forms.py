from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.utils import timezone


def past_years(ago):
    this_year = timezone.now().year
    listYears = [x for x in range(this_year, this_year - ago - 1, -1)]
    return listYears

# Custom creation form for MyUser
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MyUser
        fields = ("username", "first_name", "last_name", "email", "date_of_birth", "profile_pic")
        # date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=past_years(100)))
        widgets = {
            "date_of_birth": forms.SelectDateWidget(years=past_years(100)),
        }
