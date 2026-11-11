from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        widgets = {'categories': forms.CheckboxSelectMultiple}


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(label='Seu nome', max_length=150)

    class Meta:
        model = Comment
        fields = ['author_name', 'text']

    def get_author(self):
        User = get_user_model()
        name = self.cleaned_data['author_name'].strip()
        author = User.objects.filter(username__iexact=name).first()
        if author is None:
            author = User(username=name)
            author.set_unusable_password()
            author.save()
        return author
