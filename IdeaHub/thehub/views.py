from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

from .models import Project, Post
# Create your views here.

@login_required(login_url="login")
def home(request):
    return render(request, 'thehub/home.html')

def project(request):
	return render(request, 'thehub/project-profile.html', {"user": request.user})

def chatroom(request):
    """
    Experimenting work with django channels
    """
    return render(request, template_name="thehub/chat.html")

def room(request, room_name):
    return render(request, 'thehub/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
