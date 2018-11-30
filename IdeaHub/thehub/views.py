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
	return render(request, 'thehub/home.html', {"user": request.user, "projects":projects})

@login_required(login_url="login")
def project(request, project_name):
	projects = models.Project.objects.get_project_of_user(request.user.username)
	project = models.Project.objects.get_project_by_name(project_name)
	# Order all the post by newest first
	posts = models.Post.objects.get_parent_posts_of_project(project_name).order_by("-time_posted")


	return render(request, 'thehub/project-profile.html', {"user": request.user,
					"projects":projects,
					"project":project,
					"posts": posts})
