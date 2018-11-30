from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("<str:project_name>/", views.project, name="project"),
]
