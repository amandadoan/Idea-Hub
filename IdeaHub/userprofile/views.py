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
    template_name = "userprofile/login.html"

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
    projects = hubModels.Project.objects.get_project_of_user(request.user.username)

    posts = None
    # Get all post that the user should be involded or interested in (project member)
    for project in projects:
        project_posts = hubModels.Post.objects.get_parent_posts_of_project(project.project_name)
        if project_posts:
            if posts:
                posts = posts | project_posts
            else:
                posts = project_posts

    children_posts = {}
    if posts:
        # Remove duplicate if needed
        posts = posts.distinct().order_by("time_posted")
        # Get all children of relevant post
        for post in posts:
            post_id = post.pk
            children_posts[post_id] = hubModels.Post.objects.get_chilren_of_post(post_id)


    return render(request, 'userprofile/profile.html', {"projects":projects,
                                                        "posts": posts,
                                                        "children_posts": children_posts})
