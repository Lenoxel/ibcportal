from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
import cloudinary
from django.dispatch import receiver
from core.models import Church, Member

class EBDClass(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=50)
    description = models.CharField('Descrição', max_length=200, null=True, blank=True)
    background_image = CloudinaryField('Imagem da turma', null=True, blank=True)
    church = models.ForeignKey(Church, verbose_name='Igreja', null=True, blank=True, on_delete=models.SET_NULL)
    students = models.ManyToManyField(Member, 'Aluno')
    teachers = models.ManyToManyField(Member, 'Professor')
    secretaries = models.ManyToManyField(Member, 'Secretário')
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['name']

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=EBDClass)
def ebd_class_background_image_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.background_image.public_id)

class EBDClassLesson(models.Model):
    title = models.CharField('Lição', max_length=100)
    date = models.DateField('Data da aula')
    number = models.PositiveIntegerField('Número da aula', null=True, blank=True)
    apply_to_all = models.BooleanField('Aplicar lição a todas as classes', default=True)
    ebd_class = models.ForeignKey(EBDClass, verbose_name='Turma', on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-date']

    def __str__(self):
        return self.title