from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import Category, Comment, Post

TZ = ZoneInfo('America/Sao_Paulo')

CATEGORIES = [
    ('Automação', 'Controle, CLPs e sistemas automatizados.'),
    ('Programação', 'Linguagens, frameworks e boas práticas de código.'),
    ('Mecatrônica', 'Projetos que integram mecânica, eletrônica e computação.'),
]

POSTS = [
    {
        'title': 'Controle PID na prática',
        'date': datetime(2026, 10, 5, 14, 30, tzinfo=TZ),
        'categories': ['Automação', 'Mecatrônica'],
        'content': (
            '<p>O controlador <strong>PID</strong> é o mais usado na indústria. '
            'Ele combina três ações sobre o erro <em>e(t)</em>:</p>'
            '<ul><li><strong>P</strong>roporcional: reage ao erro atual;</li>'
            '<li><strong>I</strong>ntegral: elimina o erro em regime permanente;</li>'
            '<li><strong>D</strong>erivativa: antecipa a tendência do erro.</li></ul>'
            '<p>Na prática, começa-se ajustando o ganho proporcional e só depois '
            'se acrescentam as ações integral e derivativa.</p>'
        ),
        'comments': [
            ('ana', 'Ótimo resumo! O método de Ziegler-Nichols ajuda bastante no ajuste inicial.'),
            ('bruno', 'Vale lembrar do anti-windup quando o atuador satura.'),
            ('carla', 'Usei isso no controle de velocidade de um motor DC e funcionou muito bem.'),
        ],
    },
    {
        'title': 'Por que usar Django em aplicações web',
        'date': datetime(2026, 10, 20, 9, 0, tzinfo=TZ),
        'categories': ['Programação', 'Mecatrônica'],
        'content': (
            '<p>O <strong>Django</strong> é um framework web em Python que segue o padrão '
            '<em>MTV</em> (Model, Template, View).</p>'
            '<p>Ele já traz ORM, sistema de autenticação, painel administrativo e proteção '
            'contra CSRF, o que permite criar uma aplicação CRUD completa em pouco tempo.</p>'
        ),
        'comments': [
            ('carla', 'O painel de administração economiza muito tempo.'),
            ('ana', 'As views genéricas deixam o código bem mais curto.'),
        ],
    },
    {
        'title': 'Introdução às redes de Petri',
        'date': datetime(2026, 11, 2, 18, 45, tzinfo=TZ),
        'categories': ['Automação'],
        'content': (
            '<p>Redes de Petri modelam <strong>sistemas a eventos discretos</strong> por meio '
            'de lugares, transições e marcas (fichas).</p>'
            '<p>Com elas é possível analisar propriedades como vivacidade, limitação e '
            'reversibilidade antes de implementar o controle em um CLP.</p>'
        ),
        'comments': [],
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com categorias, posts e comentários de exemplo.'

    def handle(self, *args, **options):
        User = get_user_model()
        users = {}
        for username in ('ana', 'bruno', 'carla'):
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                user.save()
            users[username] = user

        categories = {}
        for name, description in CATEGORIES:
            categories[name], _ = Category.objects.get_or_create(name=name, defaults={'description': description})

        for data in POSTS:
            post, created = Post.objects.get_or_create(title=data['title'], defaults={'content': data['content']})
            if not created:
                continue
            Post.objects.filter(pk=post.pk).update(posted_at=data['date'])
            post.categories.set(categories[name] for name in data['categories'])
            for minutes, (username, text) in enumerate(data['comments'], start=1):
                comment = Comment.objects.create(post=post, author=users[username], text=text)
                Comment.objects.filter(pk=comment.pk).update(
                    posted_at=data['date'].replace(hour=(data['date'].hour + minutes) % 24)
                )
        self.stdout.write(self.style.SUCCESS('Banco populado.'))
