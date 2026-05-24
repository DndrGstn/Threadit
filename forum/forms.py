from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Community


class RegisterForm(UserCreationForm):
    """Form for creating a new user account."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    """Form for creating or editing a post."""

    class Meta:
        model = Post
        fields = ["title", "body", "community"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title..."}),
            "body": forms.Textarea(attrs={"placeholder": "Text (optional)", "rows": 6}),
        }


class CommentForm(forms.ModelForm):
    """Form for adding a comment to a post."""

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"placeholder": "What are your thoughts?", "rows": 4}),
        }
        labels = {"body": ""}


class CommunityForm(forms.ModelForm):
    """Form for creating a new community."""

    class Meta:
        model = Community
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "community_name"}),
            "description": forms.Textarea(attrs={"placeholder": "Tell people what this community is about.", "rows": 3}),
        }
