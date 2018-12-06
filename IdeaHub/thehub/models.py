from django.db import models
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


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
    
    def get_project_subscribed_by(self, username):
        """
        Get all projects that the given user subscribed
        """
        return self.filter(subscribers__username__iexact=username)

    def get_project_by_name(self, project_name):
        """
        Get the project using name (return a single project, not a query set)
        
        Raise: Http404 if not found
        """
        try:
            project = self.get(project_name=project_name)
            return project
        except ObjectDoesNotExist:
            raise Http404("There is no project with the given name in database")

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
    owner = models.ForeignKey("userprofile.MyUser", on_delete=models.CASCADE)
    # The owner should be added as member by the backend code
    members = models.ManyToManyField("userprofile.MyUser", related_name="projects")
    # The list of subscribers of this project, subcribers will only have the option of normal user but will get update as well
    # NOTICE: this list does not contains members and owner
    subscribers = models.ManyToManyField("userprofile.MyUser", related_name="subscriptions")

    # Set the manager of this model
    objects = ProjectManager()

    def __str__(self):
        return self.project_name

# ============================================================================================
class PostManager(models.Manager):
    """
    The custom manager to manage the database of Post
    """
    def get_posts_of_user(self, username):
        """
        Method to get all the posts of the given usename
        """
        return self.filter(user__username__iexact=username)

    def get_parent_posts_of_project(self, project_name):
        """
        Method to get all the post that are parents(direct comment) of the given project
        """
        # This query all posts that do not have parent (they are the root)
        return self.filter(project__project_name__iexact=project_name).filter(parent__isnull=True)

    def get_chilren_of_post(self, post_id):
        """
        Method to get all the children of a given post (response to that post)
        """
        return self.filter(parent__pk__iexact=post_id)


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

    # Custom manager
    objects = PostManager()

    def __str__(self):
        return self.content
