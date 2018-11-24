from django.contrib import admin
from .models import MyUser, Project, Post
from .forms import CustomUserCreationForm

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "is_superuser", "is_staff")
    list_filter = ("is_superuser", "is_staff", "is_active")

# TODO: CREATE model admin for Project and Post to manage easier

# Register your models here.
admin.site.register(MyUser, UserAdmin)
admin.site.register(Project)
admin.site.register(Post)
