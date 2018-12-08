from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from django.http import HttpResponse, JsonResponse


from . import models
from . import forms
import json

# Create your views here.

@login_required(login_url="login")
def home(request):
	projects = models.Project.objects.get_project_of_user(request.user.username)
	subscriptions = models.Project.objects.get_project_subscribed_by(request.user.username)
	categories = models.Project.objects.get_all_categories()

	return render(request, 'thehub/home.html', {"user": request.user, "projects":projects, "subscriptions": subscriptions, "categories": categories})

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


@login_required(login_url="login")
def makePost(request, project_name, parent_post_id=None):
	"""
	The view to handle creating a post. If parent is said, that means this is a response.
	"""
	user = request.user
	projects = models.Project.objects.get_project_of_user(user.username)
	current_project = models.Project.objects.get_project_by_name(project_name=project_name)

	if request.method == "GET":
		if current_project in projects:
			form = forms.MemberPostForm()
		else:
			form = forms.GeneralPostForm()
		# TODO: Change the template name
		return render(request, template_name="thehub/test.html", context={"projects": projects, "form": form, "project_name": current_project.project_name})
	elif request.method == "POST":
		form = forms.MemberPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = user
			post.project = current_project
			post.save()
			return redirect("project", project_name=current_project.project_name)


# TODO: Delete after finished testing
@login_required(login_url="login")
def test(request):
	"""
	This view is a view created for the purpose of testing methods,
	"""
	return render(request, "thehub/test.html", {"form": forms.GeneralPostForm()})


# TODO: This is the experimenting code with Ajax, transfer them into proper code
# IDEA: In order for ajax success function to know which post should be updated, we could do the following process:
# Prepare for ajax:
# 	Each post <div> should have an id ="<post_id>"
# 	Then, get all the div with class="entry" and "response" and extract their post_id
# 	Find the maximum id, because the post_id in database is auto-incremented, we will be guarantee that the largest one is the latest.
# 	Send this id as data of the ajax request back to server, along with other information such as projectname, username...
# Server side:
# 	Receive that ajax call, extract the id, and query that post from Model using its id.
#	If this is a call for user profile update, then return all posts from user's projects (subscribed and members/owner) that is newer
# 	than the current post from ajax.
# 	If this is a call for project update, do similar thing, but only get posts of that project.
# 	REMEMER TO QUERY POST WITH THE DESIRE ORDER
# 	Send back to ajax.
# Client ajax success:
# 	For each post received, check to see whehter it has a parent id
# 		If it does, then using that parent id to get the parent node from HTML DOM, and add child node properly
#		If it does not, then just put it at the top of the post section, because the list return will be sorted in desired order



def as_json(post):
	parent = post.parent.id if post.parent is not None else ""
	return dict(id=post.id,
             content=post.content,
             time_posted=str(post.time_posted),
             parent= parent,
             user=post.user.username, project=post.project.project_name)

def ajax_template(request):
	return render(request, template_name="thehub/ajax.html")

def testAjax(request, username):
	"""
	This view is a test view to deal with ajax request before using Ajax in the main project
	"""
	posts = [as_json(post) for post in models.Post.objects.get_posts_of_user(username)]

	return JsonResponse(json.dumps(posts), safe=False)
