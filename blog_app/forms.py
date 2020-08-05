from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
            'title':forms.TextInput,
            'text':forms.Textarea,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author':forms.TextInput,
            'text':forms.Textarea,
        }