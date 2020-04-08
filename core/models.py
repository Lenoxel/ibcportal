from django.conf import settings
from django.db import models
from django.utils import timezone
from enum import Enum

class MeetingCategoryEnum(Enum): 
    DOUTRINA = "Culto de Doutrina"
    EBD = "Escola Bíblica Dominical"
    INTERCESSAO = "Culto de Intercessão"
    DOMINGO = "Culto de Domingo"

class MeetingTypeEnum(Enum): 
    PRESENCIAL = "Presencial"
    ONLINE = "Online"

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
        ordering = ['-last_updated_date']

    def __str__(self):
        return self.title

class Publisher(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', max_length=300)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'membros'
        ordering = ['name']

    def __str__(self):
        return self.name

class PostFile(models.Model):
    post = models.ForeignKey('core.Post', verbose_name='Postagem', on_delete=models.CASCADE, related_name='files')
    file = models.FileField('Arquivo', upload_to='post_files/')
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)

class PostView(models.Model):
    objects = models.Manager()

    post = models.OneToOneField(Post, verbose_name='Postagem', on_delete=models.CASCADE)
    views_count = models.IntegerField('Visualizações', default=0)

    class Meta:
        verbose_name = 'Visualização'
        verbose_name_plural = 'Visualizações'
        ordering = ['-views_count']

    def __str__(self):
        if self.views_count > 1:
            return "{} - {} visualizações".format(self.post, self.views_count)
        else:
            return "{} - {} visualização".format(self.post, self.views_count)

class Video(models.Model):
    objects = models.Manager()

    src = models.CharField('URL', max_length=100)
    category = models.CharField('Categoria', max_length=15, choices=[(meetingCategory.name, meetingCategory.value) for meetingCategory in MeetingCategoryEnum])
    title = models.CharField('Título do vídeo', max_length=100)
    description = models.TextField('Descrição do vídeo', max_length=300, null = True, blank = True)
    registering_date = models.DateTimeField('Cadastrado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Vídeo'
        verbose_name_plural = 'Vídeos'
        ordering = ['-registering_date']

    def __str__(self):
        return self.title

class Schedule(models.Model):
    objects = models.Manager()

    title = models.CharField('Encontro', max_length=15, choices=[(meetingCategory.name, meetingCategory.value) for meetingCategory in MeetingCategoryEnum])
    start_date = models.DateTimeField('Horário de início')
    end_date = models.DateTimeField('Horário de fim', null=True, blank=True)
    location = models.ForeignKey('core.Church', verbose_name='Local', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField('Descrição', max_length=300, blank=True, null=True)
    preacher = models.ForeignKey('core.Publisher', verbose_name='Pregador', null=True, on_delete=models.SET_NULL)
    organizing_group = models.ForeignKey('core.Group', verbose_name='Grupo Organizador', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.CharField('Tipo', max_length=15, choices=[(meetingType.name, meetingType.value) for meetingType in MeetingTypeEnum])
    # does_repeat = models.BooleanField('Se repete', default=False)
    # repetition_quantity = models.IntegerField('Quantidade de repetições semanais', default=0)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Encontro'
        verbose_name_plural = 'Agenda'
        ordering = ['-start_date']

    def __str__(self):
        if self.end_date:
            start_date = self.start_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            end_date = self.end_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            formatted_start_hour = start_date.strftime("%X")[0:5]
            formatted_end_hour = end_date.strftime("%X")[0:5]
            return '{}: {} - {} às {}'.format(self.title, start_date.strftime("%x"), formatted_start_hour, formatted_end_hour)
        else:
            date = self.start_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            formatted_hour = date.strftime("%X")[0:5]
            return '{}: {} - {}'.format(self.title, date.strftime("%x"), formatted_hour)

class Group(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    leader = models.ForeignKey('core.Publisher', verbose_name='Líder', related_name='group_leader', null=True, on_delete=models.SET_NULL)
    vice_leader = models.ForeignKey('core.Publisher', verbose_name='Vice-líder', related_name='vice_leader', null=True, blank=True, on_delete=models.SET_NULL)
    third_leader = models.ForeignKey('core.Publisher', verbose_name='Terceiro líder', related_name='third_leader', null=True, blank=True, on_delete=models.SET_NULL)
    background_image = models.ImageField('Imagem do grupo', upload_to ='group_images/')
    church = models.ForeignKey('core.Church', verbose_name='Igreja', null=True, blank=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']

    def __str__(self):
        return self.name

class Church(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    address = models.CharField('Endereço', max_length=250)
    chief_pastor = models.ForeignKey('core.Publisher', verbose_name='Pastor Principal', null=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Igreja'
        verbose_name_plural = 'Igrejas'
        ordering = ['name']

    def __str__(self):
        return self.name