from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Project, Post
# Create your views here.

@login_required
def home(request):
    return render(request, 'thehub/home.html')
