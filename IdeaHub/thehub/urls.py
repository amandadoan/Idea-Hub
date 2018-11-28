from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("chat/", views.chatroom, name="chatroom"),
    path("chat/<str:room_name>", views.room, name="room"),
    path("project", views.project, name="project"),
]
