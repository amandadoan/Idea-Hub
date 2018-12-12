from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from django.views import generic
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from thehub import models as hubModels


# Create your views here.

# Sign up view, using built-in class based view so it is easier to maintain and deploy
# Read more here: https://docs.djangoproject.com/en/2.0/topics/class-based-views/intro/
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "userprofile/signup.html"

    def get(self, request):
        # Customize the get method, the post method is handled for us by built-in function

        if request.user.is_authenticated:
            # Redirect user to the profile page if they already login and try to sign up
            return redirect("profile")
        else:
            form = self.form_class()
            return render(request, self.template_name, {"form": form})


@login_required(login_url="login", redirect_field_name="profile")
def profile(request):
    user = request.user
    projects = hubModels.Project.objects.get_project_of_user(user.username)
    subscriptions = hubModels.Project.objects.get_project_subscribed_by(user.username)

    # Get all post that the user should be involded or interested in (project member)
    # THIS SHOULD INCLUDE PROJECTS IN SUBSCRIPTIONS AS WELL
    posts = hubModels.Post.objects.get_parent_posts_user_interested(user.username)
    children_posts = {}

    if posts:
        posts = posts.order_by("-id")
        # Get all children of relevant post
        for post in posts:
            post_id = post.pk
            # Let's children post be ordered by oldest first to make a flow for the conversation
            children_posts[post_id] = hubModels.Post.objects.get_chilren_of_post(post_id)

    owned_projects = hubModels.Project.objects.get_project_owned_by(user.username)
    pending_requests = None
    for project in owned_projects:
        if pending_requests is None:
            pending_requests = hubModels.MemberRequest.objects.get_requests_for_project(project)
        else:
            pending_requests = pending_requests | hubModels.MemberRequest.objects.get_requests_for_project(project)

    return render(request, 'userprofile/profile.html', {"projects":projects,
                                                        "subscriptions": subscriptions,
                                                        "posts": posts,
                                                        "children_posts": children_posts,
                                                        "pending_requests": pending_requests})
