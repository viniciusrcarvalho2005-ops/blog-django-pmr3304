from django import forms
from django.contrib.auth import get_user_model

from .models import Comment


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(label='Seu nome', max_length=150)

    class Meta:
        model = Comment
        fields = ['author_name', 'text']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        # Quem está logado comenta com a própria conta e não precisa digitar o nome
        if user is not None and user.is_authenticated:
            del self.fields['author_name']

    def clean_author_name(self):
        name = self.cleaned_data['author_name'].strip()
        existing = get_user_model().objects.filter(username__iexact=name).first()
        if existing and existing.has_usable_password():
            raise forms.ValidationError(
                'Esse nome pertence a uma conta cadastrada. Entre na conta para usá-lo ou escolha outro nome.'
            )
        return name

    def get_author(self):
        """Usuário do Django que será o autor: a conta logada ou um usuário criado a partir do nome."""
        if 'author_name' not in self.fields:
            return self.user
        User = get_user_model()
        name = self.cleaned_data['author_name']
        author = User.objects.filter(username__iexact=name).first()
        if author is None:
            author = User(username=name)
            author.set_unusable_password()
            author.save()
        return author
