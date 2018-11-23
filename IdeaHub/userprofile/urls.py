from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="userprofile/login.html"), name="login"),
    path("signup/", views.SignUp.as_view(), name="signup")
]
