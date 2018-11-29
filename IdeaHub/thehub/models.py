from django.db import models
from django.db.models import Q


# Create your models here.
class ProjectManager(models.Manager):
    """
    The custom manager to provide higher level API for the Project objects
    """
    def get_all_projects(self):
        """
        Get all projects in the database
        """
        return self.all()

    def get_project_of_user(self, username):
        """
        Get all projects (members and owner) of the given user
        """
        return (self.filter(members__username__iexact=username)
                | self.filter(owner__username__iexact=username)).distinct()

    def get_project_owned_by(self, username):
        """
        Get all projects that the given user owned
        """
        return self.filter(owner__username__iexact=username)

class Project(models.Model):
    """
    The model for project object
    """
    # Basic information of Project
    project_name = models.CharField(max_length=150, blank=False, primary_key=True)
    description = models.TextField(max_length=None, blank=False)
    created_date = models.DateTimeField(verbose_name="Created date", auto_now_add=True)
    end_date = models.DateTimeField(verbose_name="Ended date")
    # Category
    CATEGORIES = (("Designing", "Designing"),
                    ("Coding", "Coding"),
                    ("Cooking", "Cooking"),
                    ("Photography", "Photography"),
                    ("Writing", "Writing"),
                    ("Traveling", "Traveling"),
                    ("Other", "Other"))
    category = models.CharField(choices=CATEGORIES, default="Other", max_length=20)

    # The owner is the person who creatde the project, whereas the members are ones participating in the project
    owner = models.OneToOneField("userprofile.MyUser", on_delete=models.CASCADE)
    # The owner should be added as member by the backend code
    members = models.ManyToManyField("userprofile.MyUser", related_name="projects")

    # Set the manager of this model
    objects = ProjectManager()

    def __str__(self):
        return self.project_name


class Post(models.Model):
    """
    The model for a post. A post can be a comment, a question, or an update on the current project
    """

    TYPES = (("Q", "Question"), ("C", "Comment"), ("U", "Update"))

    # Not allowed post without content
    content = models.TextField(blank=False)
    type = models.CharField(choices=TYPES, blank=False, default="C", max_length=2)
    # Auto assigned the created time
    time_posted = models.DateTimeField(auto_now_add=True)

    # TODO: A parent post can have many child comments/
    parent = models.ForeignKey("Post", on_delete=models.CASCADE, blank=True, null=True)

    # The user and project this post belongs to
    user = models.ForeignKey("userprofile.MyUser", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __str__(self):
        return self.content
