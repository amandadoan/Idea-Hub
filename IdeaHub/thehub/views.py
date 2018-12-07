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
	

