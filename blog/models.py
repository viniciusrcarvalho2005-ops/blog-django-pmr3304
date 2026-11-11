from django.db import models


class Post(models.Model):
    title = models.CharField('título', max_length=200)
    content = models.TextField('conteúdo (HTML)')
    posted_at = models.DateTimeField('data de postagem', auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return self.title
