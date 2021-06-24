from typing import Text
from django.forms import ModelForm, Textarea
from django.forms.widgets import TextInput, EmailInput
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'email', 'content']
        
        comment_field = {'class': 'form-control my-2 comment-field'}
        widgets = {
            'author': TextInput(attrs=comment_field),
            'email': EmailInput(attrs=comment_field),
            'content': Textarea(attrs={'rows': 5, 'class': 'form-control my-2'}),
        }