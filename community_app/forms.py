from django import forms

from .models import Comment, CommunityPost


class CommunityPostForm(forms.ModelForm):

    class Meta:
        model = CommunityPost

        fields = (
            "title",
            "body",
            "image",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control pet-input",
                    "placeholder": "Give your post a clear title",
                }
            ),

            "body": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 7,
                    "placeholder": (
                        "Share your question, experience, "
                        "story or pet-care advice..."
                    ),
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control pet-input",
                    "accept": "image/*",
                }
            ),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = (
            "body",
        )

        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control pet-input",
                    "rows": 3,
                    "placeholder": "Write a helpful comment...",
                }
            ),
        }