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
	user = request.user
	all_projects = models.Project.objects.get_all_projects()
	projects = models.Project.objects.get_project_of_user(user.username)
	subscriptions = models.Project.objects.get_project_subscribed_by(user.username)
	categories = models.Project.objects.get_all_categories()

	return render(request, 'thehub/home.html', {"user": request.user,
												"all_projects": all_projects,
												"projects":projects, 
												"subscriptions": subscriptions, 
												"categories": categories})

@login_required(login_url="login")
def project(request, project_name):
	projects = models.Project.objects.get_project_of_user(request.user.username)
	subscriptions = models.Project.objects.get_project_subscribed_by(request.user.username)


	project = models.Project.objects.get_project_by_name(project_name)
	# Order all the post by newest first
	posts = models.Post.objects.get_parent_posts_of_project(project_name)

	children_posts = {}
	if posts:
		posts = posts.order_by("-id")
        # Get all children of relevant post
		for post in posts:
			# Let's children post be ordered by oldest first to make a flow for the conversation
			children_posts[post.id] = models.Post.objects.get_chilren_of_post(post.id)

	return render(request, 'thehub/project-profile.html', {"projects":projects,
                    										"subscriptions": subscriptions,
															"project":project,
															"posts": posts,
															"children_posts": children_posts})


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
	"""
	Convert the current post model into a dictionary so it can be passed as json data 
	"""
	parent = post.parent.id if post.parent is not None else ""
	return dict(id=post.id,
             content=post.content,
             time_posted=str(post.time_posted),
             parent= parent,
			 type = post.get_type_display(),
             user=post.user.username, project=post.project.project_name)

def ajax_template(request):
	return render(request, template_name="thehub/ajax.html")

@login_required(login_url="login")
def getUserUpdate(request, username, post_id=None):
	"""
	This view is a used to deal with ajax request for user profile update
	"""
	# Sort post in ascending order of id, so the older view will be update to front end first when doing looping
	if post_id is None:
		return JsonResponse({})
	query_posts = [post for post in models.Post.objects.get_post_user_intested(username)
											.filter(id__gt=post_id)
											.order_by("id")]
	
	update_posts = [as_json(post) for post in query_posts]
	return JsonResponse(json.dumps(update_posts), safe=False)

@login_required(login_url="login")
def getProjectUpdate(request, project_name, post_id=None):
	"""
	This view is used to handle ajax request for getting new posts updated from ajax.
	"""
	# TODO: The project update response should also include update regarding new member as well.
	# This handles the base case where no post_id is specified to look up
	if post_id is None:
		return JsonResponse({})
	else:
		posts = [as_json(post) for post in models.Post.objects
												.get_all_posts_of_project(project_name)
												.filter(id__gt=post_id)
												.order_by("-id")]
		return JsonResponse(json.dumps(posts), safe=False)
	
