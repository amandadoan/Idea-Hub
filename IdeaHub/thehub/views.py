from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from . import models
from . import forms
# Create your views here.

@login_required(login_url="login")
def home(request):
	projects = models.Project.objects.get_project_of_user(request.user.username)
	subscriptions = models.Project.objects.get_project_subscribed_by(request.user.username)

	return render(request, 'thehub/home.html', {"user": request.user, "projects":projects, "subscriptions": subscriptions})

@login_required(login_url="login")
def project(request, project_name):
	projects = models.Project.objects.get_project_of_user(request.user.username)
	subscriptions = models.Project.objects.get_project_subscribed_by(request.user.username)


	project = models.Project.objects.get_project_by_name(project_name)
	# Order all the post by newest first
	posts = models.Post.objects.get_parent_posts_of_project(project_name).order_by("-time_posted")

	return render(request, 'thehub/project-profile.html', {"user": request.user,
					"projects":projects,
                    "subscriptions": subscriptions,
					"project":project,
					"posts": posts})

# TODO: Delete after finished testing
@login_required(login_url="login")
def test(request):
	"""
	This view is a view created for the purpose of testing methods,
	"""
	return render(request, "thehub/test.html", {"form": forms.GeneralPostForm()})
