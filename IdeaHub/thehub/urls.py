from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("thehub/project/<str:project_name>/", views.project, name="project"),
    path("thehub/post/", views.makePost, name="makePost"),
    path("thehub/post/<str:project_name>/", views.makePost, name="makePost"),
    path("thehub/post/<str:project_name>/<int:parent_post_id>", views.makePost, name="makePost"),

    # The path without post_id is used to make sure template can be rendered without error
    path("thehub/getprojectupdate/<str:project_name>/<int:post_id>", views.getProjectUpdate, name="ajaxProjectUpdate"),
    path("thehub/getprojectupdate/<str:project_name>/", views.getProjectUpdate, name="ajaxProjectUpdate"),
    path("thehub/getuserupdate/<str:username>/<int:post_id>", views.getUserUpdate, name="ajaxUserUpdate"),
    path("thehub/getuserupdate/<str:username>/", views.getUserUpdate, name="ajaxUserUpdate"),
    # Filter by category
    path("thehub/filterByCategory/<str:category>/", views.filterProjectByCategory, name="filterByCategory"),
    # Search projects with given keywords, the empty parameter url is for initial rendering the page
    path("thehub/search/<str:keywords>/", views.searchProjectsByKeywords, name="searchProjects"),
    path("thehub/search/", views.searchProjectsByKeywords, name="searchProjects"),
    # Subscribe or unsubscribe url
    path("thehub/subscription/<str:project_name>/", views.manageSubscription, name="manageSubscription"),
    # Ask to join or leave as member
    path("thehub/memberrequest/<str:project_name>/", views.manageMemberRequest, name="memberrequest"),
    # Test path
    path("test/", views.test, name="test"),
    path("ajax/", views.ajax_template, name="ajax_template"),
    # path("ajax_request/<str:username>/", views.testAjax, name="ajax")
]
