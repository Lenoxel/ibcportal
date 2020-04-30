from django.db import models
from cloudinary.models import CloudinaryField

class Group(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    leader = models.ForeignKey('core.Member', verbose_name='Líder', related_name='group_leader', null=True, on_delete=models.SET_NULL)
    vice_leader = models.ForeignKey('core.Member', verbose_name='Vice-líder', related_name='vice_leader', null=True, blank=True, on_delete=models.SET_NULL)
    third_leader = models.ForeignKey('core.Member', verbose_name='Terceiro líder', related_name='third_leader', null=True, blank=True, on_delete=models.SET_NULL)
    background_image = CloudinaryField('Imagem do grupo')
    church = models.ForeignKey('core.Church', verbose_name='Igreja', null=True, blank=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']

    def __str__(self):
        return self.name

