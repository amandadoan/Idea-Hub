from django import forms
from .models import Post

class MemberPostForm(forms.ModelForm):
    """
    Form to create a new post for a project as a member. This post is parent-level postself.
    There will be the option to post as update.
    All information of user and project should be populated by the view's backend code
    """
    class Meta:
        model = Post
        # In all cases, project should be prefilled by view's backend code
        fields = ["content", "type", "project"]


class GeneralPostForm(forms.ModelForm):
    """
    Form to create a post for general user, this only include the option to post as comment or question, not update post.
    This form allows to choose which project to post.
    """
    class Meta:
        model = Post
        # Project should be prefilled by view's backend code
        fields = ["content", "type", "project"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].choices = (("Q", "Question"), ("C", "Comment"))

class ReponsePostForm(forms.ModelForm):
    """
    Form to create a response. This form is similar to GeneralPostForm, but without the ability to choose project.
    When using this form, the view's backend code should added the value for parent.
    """
    class Meta:
        model = Post
        fields = ["content", "type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].choices = (("Q", "Question"), ("C", "Comment"))
    
