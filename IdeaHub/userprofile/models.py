from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    The user model for the whole application. Also can be used in the admin interface.
    Extending PermissionsMixin to grant the proper permission to different type of users
    """

    # Basic information of user
    username = models.CharField(max_length=40, unique=True, blank=False)
    first_name = models.CharField(max_length=40, blank=False)
    last_name = models.CharField(max_length=40, blank=False)
    email = models.EmailField(blank=False)
    # The profile picture and the date of birth can be i=empty
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)

    # Management variables for django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)

    # The manager to control the objects created using this model
    objects = UserManager()
    # The identifier of this model in the database, using username for simplicity
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    # Must-have information when creating an account
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self):
        return self.first_name + " " + self.last_name + " ({})".format(self.username)

class Project(models.Model):
    """
    The model for project object
    """
    # Basic information of Project
    project_name = models.CharField(max_length=150, blank=False, primary_key=True)
    description = models.TextField(max_length=None, blank=False)
    created_date = models.DateTimeField(verbose_name="Created date", auto_now_add=True)
    end_date = models.DateTimeField(verbose_name="Ended date")
    # The owner is the person who creatde the project, whereas the members are ones participating in the project
    owner = models.OneToOneField("MyUser", on_delete=models.CASCADE)
    members = models.ManyToManyField("MyUser", related_name="projects")

    def __str__(self):
        return self.project_name

class Post(models.Model):
    """
    The model for a post. A post can be a comment, a question, or an update on the current project
    """

    TYPES = [("Q", "Question"), ("C", "Comment"), ("U", "Update")]

    # Not allowed post without content
    content = models.TextField(blank=False)
    type = models.CharField(choices=TYPES, blank=False, default="C", max_length=2)
    # Auto assigned the created time
    time_posted = models.DateTimeField(auto_now_add=True)

    # The user and project this post belongs to
    user = models.ForeignKey("MyUser", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __str__(self):
        return self.content
