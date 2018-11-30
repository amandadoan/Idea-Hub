from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from . import models

from .models import Project, Post
# Create your views here.

@login_required(login_url="login")
def home(request):
	projects = models.Project.objects.get_project_of_user(request.user.username)
	return render(request, 'thehub/home.html', {"projects":projects})

def project(request, project_name):
	projects = models.Project.objects.get_project_of_user(request.user.username)
	project = models.Project.objects.get_project_by_name(project_name)
	posts = models.Post.objects.get_parent_posts_of_project(project_name)

	return render(request, 'thehub/project-profile.html', {"user": request.user,
					"projects":projects,
					"project":project,
					"posts": posts})

def chatroom(request):
    """
    Experimenting work with django channels
    """
    return render(request, template_name="thehub/chat.html")

def room(request, room_name):
    return render(request, 'thehub/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
