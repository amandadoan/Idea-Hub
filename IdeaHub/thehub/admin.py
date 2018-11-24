from django.contrib import admin
from .models import Project, Post


# TODO: CREATE model admin for Project and Post to manage easier

# Register your models here.
admin.site.register(Project)
admin.site.register(Post)
