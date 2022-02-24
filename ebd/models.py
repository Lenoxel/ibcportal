from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
import cloudinary
from django.dispatch import receiver
from core.models import DEFAULT_CHURCH_ID, Church, Member
# from ibcportal import settings
from django.conf import settings

from pynamodb.models import Model
# from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute, UTCDateTimeAttribute
from django.contrib.auth.models import User

class EBDClass(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=50)
    description = models.CharField('Descrição', max_length=200, null=True, blank=True)
    background_image = CloudinaryField('Imagem da turma', null=True, blank=True)
    church = models.ForeignKey(Church, verbose_name='Igreja', null=True, blank=True, on_delete=models.SET_NULL)
    students = models.ManyToManyField(Member, related_name='Aluno', verbose_name='Alunos', blank=True)
    teachers = models.ManyToManyField(Member, related_name='Professor', verbose_name='Professores', blank=True)
    secretaries = models.ManyToManyField(Member, related_name='Secretário', verbose_name='Secretários', blank=True)
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

class EBDLesson(models.Model):
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

class EBDPresenceRecord(models.Model):
    lesson = models.ForeignKey(EBDLesson, verbose_name='Lição', on_delete=models.CASCADE)
    student = models.ForeignKey(Member, related_name='student_presence_record', verbose_name='Aluno', on_delete=models.CASCADE)
    ebd_class = models.ForeignKey(EBDClass, verbose_name='Classe', on_delete=models.SET_NULL, blank=True, null=True)
    ebd_church = models.ForeignKey(Church, verbose_name='Igreja', on_delete=models.SET_NULL, blank=True, null=True, default=DEFAULT_CHURCH_ID)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name='Criado por', null=True, on_delete=models.SET_NULL)
    attended = models.BooleanField('Presente', default=False)
    register_on = models.DateTimeField('Registro em', blank=True, null=True)
    # register_by = models.ForeignKey(User, verbose_name='Última atualização por', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Registro de Presença'
        verbose_name_plural = 'Registro de Presenças'
        ordering = ['-creation_date']

    def __str__(self):
        return '{} - {} ({})'.format(self.lesson.date.strftime('%d/%m/%Y'), self.student, self.ebd_class)

    def initialize_object(self, ebdPresenceRecordObject):
        self.lesson = ebdPresenceRecordObject.get('lesson')
        self.student = ebdPresenceRecordObject.get('student')
        self.ebd_class = ebdPresenceRecordObject.get('ebd_class')
        self.created_by = ebdPresenceRecordObject.get('created_by')


# Below: dynamoDB - EBD lesson presence record

# class UserIdIndex(GlobalSecondaryIndex):
#     user_id = UnicodeAttribute(hash_key=True)

#     class Meta:
#         read_capacity_units = 1
#         write_capacity_units = 1
#         projection = AllProjection()

# class ClassIdIndex(GlobalSecondaryIndex):
#     class_id = UnicodeAttribute(hash_key=True)
#     lesson_date = UnicodeAttribute(range_key=True)

#     class Meta:
#         read_capacity_units = 1
#         write_capacity_units = 1
#         projection = AllProjection()

# class ChurchLessonDateIndex(GlobalSecondaryIndex):
#     church = UnicodeAttribute(hash_key=True)
#     lesson_date = UnicodeAttribute(range_key=True)

#     class Meta:
#         read_capacity_units = 1
#         write_capacity_units = 1
#         projection = AllProjection()

# class EBDLessonPresenceRecord(Model):
#     lesson_date = UnicodeAttribute(hash_key=True)
#     user_id = UnicodeAttribute(range_key=True)
#     class_id = UnicodeAttribute()
#     lesson_name = UnicodeAttribute()
#     class_name = UnicodeAttribute()
#     church = UnicodeAttribute()
#     created_by = UnicodeAttribute()
#     creation_date = UTCDateTimeAttribute()
#     attended = BooleanAttribute(null=True)
#     register_on = UnicodeAttribute(null=True)
#     register_by = UnicodeAttribute(null=True)

#     user_id_index = UserIdIndex()
#     class_id_index = ClassIdIndex()
#     church_lesson_date_index = ChurchLessonDateIndex()

#     class Meta:
#         aws_access_key_id = settings.AWS_ACCESS_KEY_ID
#         aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
#         table_name = 'IBCProject-EBDLessonPresenceRecord'
#         region = 'us-west-2'
#         verbose_name = 'Registro de Presença na aula'
#         verbose_name_plural = 'Registros de Presença nas aulas'

#     def __str__(self):
#         return '{} - {} - {}'.format(self.lesson_date, self.class_id, self.user_id)
