from django import forms
from django.contrib.auth import get_user_model

from .models import Comment


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(label='Seu nome', max_length=150)

    class Meta:
        model = Comment
        fields = ['author_name', 'text']

    def get_author(self):
        """Usuário do Django com o nome informado; é criado se ainda não existir."""
        User = get_user_model()
        name = self.cleaned_data['author_name'].strip()
        author = User.objects.filter(username__iexact=name).first()
        if author is None:
            author = User(username=name)
            author.set_unusable_password()
            author.save()
        return author
