from django import forms
from .models import Post

class ProjectPostForm(forms.ModelForm):
    """
    Form to create a new post for a project. This post is parent-level postself.
    All information of user and project should be populated by the view's backend code
    """
    class Meta:
        model = Post
        # In all cases, project should be prefilled by view's backend code
        fields = ["content", "type", "project"]
