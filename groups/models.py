from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
import cloudinary
from django.dispatch import receiver
from core.models import Member

DAY_OPTIONS = [
    ('Segunda', 'Segunda'),
    ('Terça', 'Terça'),
    ('Quarta', 'Quarta'),
    ('Quinta', 'Quinta'),
    ('Sexta', 'Sexta'),
    ('Sábado', 'Sábado'),
    ('Domingo', 'Domingo'),
]

class GeneralCategory(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    icon = CloudinaryField('Ícone da categoria')
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Categoria de Grupo'
        verbose_name_plural = 'Categorias de grupo'
        ordering = ['name']

    def __str__(self):
        return self.name
class Group(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    description = models.CharField('Descrição', max_length=100)
    info = models.TextField('Info')
    general_category = models.ForeignKey('groups.GeneralCategory', verbose_name='Categoria', null=True, on_delete=models.SET_NULL)
    leader = models.ForeignKey('core.Member', verbose_name='Líder', related_name='group_leader', null=True, on_delete=models.SET_NULL)
    another_leader = models.ForeignKey('core.Member', verbose_name='Outro líder', related_name='another_group_leader', null=True, on_delete=models.SET_NULL)
    vice_leader = models.ForeignKey('core.Member', verbose_name='Vice-líder', related_name='vice_leader', null=True, blank=True, on_delete=models.SET_NULL)
    another_vice_leader = models.ForeignKey('core.Member', verbose_name='Outro vice-líder', related_name='another_vice_leader', null=True, on_delete=models.SET_NULL)
    third_leader = models.ForeignKey('core.Member', verbose_name='Terceiro líder', related_name='third_leader', null=True, blank=True, on_delete=models.SET_NULL)
    background_image = CloudinaryField('Imagem do grupo')
    church = models.ForeignKey('core.Church', verbose_name='Igreja', null=True, blank=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(Member, 'Membro')
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Group)
def group_background_image_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.background_image.public_id)

class GroupMeetingDate(models.Model):
    group = models.ForeignKey('groups.Group', verbose_name='Grupo', on_delete=models.CASCADE, related_name='meeting_dates')
    title = models.CharField('Tipo do encontro', max_length=100, null=True, blank=True)
    day = models.CharField('Dia', choices=DAY_OPTIONS, max_length=20)
    start_date = models.TimeField('Início')
    end_date = models.TimeField('Fim', null=True, blank=True)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Horário'
        verbose_name_plural = 'Horários'
        ordering = ['-day']

    def __str__(self):
        if self.end_date:
            return '{} - {}, {} às {}'.format(self.group, self.day, self.start_date, self.end_date)
        else:
            return '{} - {}, {}'.format(self.group, self.day, self.start_date)

