from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("thehub/project/<str:project_name>/", views.project, name="project"),
    path("thehub/post/<str:project_name>", views.makePost, name="makePost"),
    # Test path
    path("test/", views.test, name="test"),
    path("ajax/", views.ajax_template, name="ajax_template"),
    path("ajax_request/<str:username>/", views.testAjax, name="ajax")
]
