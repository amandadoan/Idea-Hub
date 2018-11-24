from django.db import models

# Create your models here.
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
    owner = models.OneToOneField("userprofile.MyUser", on_delete=models.CASCADE)
    members = models.ManyToManyField("userprofile.MyUser", related_name="projects")

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
    user = models.ForeignKey("userprofile.MyUser", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __str__(self):
        return self.content
