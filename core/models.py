from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    objects = models.Manager()

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Gerenciador', null=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey('core.Publisher', verbose_name='Publicador', null=True, on_delete=models.SET_NULL)
    title = models.CharField('Título da postagem', max_length=200)
    text = models.TextField('Texto da postagem')
    to_notify = models.BooleanField('Notificar', default=False)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    published_date = models.DateTimeField('Publicado em', blank=True, null=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'
        ordering = ['published_date']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Publisher(models.Model):
    objects = models.Manager()

    name = models.CharField('Pessoa', max_length=60)
    description = models.TextField('Descrição', max_length=300)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Publicador'
        verbose_name_plural = 'Publicadores'
        ordering = ['name']

    def __str__(self):
        return self.name

