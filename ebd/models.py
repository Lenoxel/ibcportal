import cloudinary
from cloudinary.models import CloudinaryField

# from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
# from pynamodb.attributes import BooleanAttribute, UnicodeAttribute, UTCDateTimeAttribute
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from core.models import DEFAULT_CHURCH_ID, Church, Member

# from ibcportal import settings
# from django.conf import settings


EBD_PRESENCE_RECORD_LABEL_OPTIONS = [
    ("positive", "Positivo"),
    ("negative", "Negativo"),
    ("neutral", "Neutro"),
]


class EBDClass(models.Model):
    name = models.CharField("Nome", max_length=50)
    description = models.CharField("Descrição", max_length=200, null=True, blank=True)
    background_image = CloudinaryField("Imagem da classe", null=True, blank=True)
    church = models.ForeignKey(
        Church, verbose_name="Igreja", null=True, blank=True, on_delete=models.SET_NULL
    )
    students = models.ManyToManyField(
        Member, related_name="student", verbose_name="Alunos", blank=True
    )
    teachers = models.ManyToManyField(
        Member, related_name="teacher", verbose_name="Professores", blank=True
    )
    secretaries = models.ManyToManyField(
        Member, related_name="secretary", verbose_name="Secretários", blank=True
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=EBDClass)
def ebd_class_background_image_delete(sender, instance, **kwargs):
    if instance.background_image and instance.background_image.public_id:
        cloudinary.uploader.destroy(instance.background_image.public_id)


class EBDLesson(models.Model):
    magazine_title = models.CharField("Revista", max_length=100, null=True, blank=True)
    title = models.CharField("Lição", max_length=100)
    date = models.DateField("Data da lição")
    number = models.PositiveIntegerField("Número da lição", null=True, blank=True)
    single_class = models.BooleanField("Classe Única", default=False)
    apply_to_all = models.BooleanField("Aplicar lição a todas as classes", default=True)
    ebd_class = models.ForeignKey(
        EBDClass, verbose_name="Classe", on_delete=models.CASCADE, null=True, blank=True
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Lição"
        verbose_name_plural = "Lições"
        ordering = ["-date"]

    def __str__(self):
        lesson_date = self.date.strftime("%d/%m/%Y")
        return (
            "{} - {}".format(lesson_date, self.title)
            if self.apply_to_all
            else "{} - {} ({})".format(lesson_date, self.title, self.ebd_class)
        )


class EBDLessonClassDetails(models.Model):
    lesson = models.ForeignKey(
        EBDLesson, verbose_name="Lição", on_delete=models.CASCADE
    )
    ebd_class = models.ForeignKey(
        EBDClass, verbose_name="Classe", on_delete=models.CASCADE
    )
    visitors_quantity = models.PositiveIntegerField("Número de visitantes", default=0)
    money_raised = models.FloatField("Dinheiro arrecadado", null=True, blank=True)
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Detalhes da classe na lição"
        verbose_name_plural = "Detalhes das classes nas lições"
        ordering = ["-last_updated_date"]

    def __str__(self):
        return "{} - {}".format(self.lesson, self.ebd_class)

    def save_details(self, ebd_class_lesson_details_object):
        self.visitors_quantity = (
            ebd_class_lesson_details_object.get("visitors_quantity") or 0
        )
        self.money_raised = ebd_class_lesson_details_object.get("money_raised") or None
        self.save()


class EBDPresenceRecord(models.Model):
    lesson = models.ForeignKey(
        EBDLesson, verbose_name="Lição", on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        Member,
        related_name="person_presence_record",
        verbose_name="Pessoa",
        on_delete=models.CASCADE,
    )
    ebd_class = models.ForeignKey(
        EBDClass,
        verbose_name="Classe",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    ebd_church = models.ForeignKey(
        Church,
        verbose_name="Igreja",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=DEFAULT_CHURCH_ID,
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        verbose_name="Criado por",
        related_name="presence_record_created_by",
        null=True,
        on_delete=models.SET_NULL,
    )
    attended = models.BooleanField("Presente", default=False)
    justification = models.CharField(
        "Justificativa da Falta", max_length=500, null=True, blank=True
    )
    register_on = models.DateTimeField("Registro em", blank=True, null=True)
    register_by = models.ForeignKey(
        User,
        verbose_name="Última atualização por",
        related_name="presence_record_register_by",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Registro de Presença"
        verbose_name_plural = "Registro de Presenças"
        ordering = ["-creation_date"]
        # unique_together = ('lesson', 'ebd_class', 'person')

    def __str__(self):
        return "{} - {} ({})".format(
            self.lesson.date.strftime("%d/%m/%Y"), self.person, self.ebd_class
        )

    def initialize_object(self, ebd_presence_record_object):
        self.lesson = ebd_presence_record_object.get("lesson")
        self.person = ebd_presence_record_object.get("person")
        self.ebd_class = ebd_presence_record_object.get("ebd_class")
        self.created_by = ebd_presence_record_object.get("created_by")

    def save_presence_record(self, ebd_presence_record_object, user):
        self.attended = ebd_presence_record_object.get("attended") or False
        self.justification = ebd_presence_record_object.get("justification") or None
        self.register_on = ebd_presence_record_object.get("register_on") or None
        self.register_by = user

        self.save()


class EBDLabelOptions(models.Model):
    title = models.CharField("Label", max_length=100)
    type = models.CharField(
        "Tipo",
        choices=EBD_PRESENCE_RECORD_LABEL_OPTIONS,
        max_length=30,
        null=True,
        blank=True,
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Etiqueta de EBD"
        verbose_name_plural = "Etiquetas de EBD"
        ordering = ["title"]

    def __str__(self):
        return self.title


class EBDPresenceRecordLabels(models.Model):
    ebd_presence_record = models.ForeignKey(
        EBDPresenceRecord,
        related_name="ebd_presence_record",
        verbose_name="Registro de Presença",
        on_delete=models.CASCADE,
    )
    ebd_label_option = models.ForeignKey(
        EBDLabelOptions,
        related_name="ebd_label_option",
        verbose_name="Label",
        on_delete=models.CASCADE,
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Etiqueta de aluno na EBD"
        verbose_name_plural = "Etiquetas dos alunos na EBD"
        ordering = ["-last_updated_date"]

    def __str__(self):
        return "Em {}, {} recebeu o label {}".format(
            self.ebd_presence_record.lesson.date.strftime("%d/%m/%Y"),
            self.ebd_presence_record.person,
            self.ebd_label_option,
        )

    def save_presence_record_label(self, ebd_presence_record_label_object):
        self.ebd_presence_record = ebd_presence_record_label_object.get(
            "ebd_presence_record"
        )
        self.ebd_label_option = ebd_presence_record_label_object.get("ebd_label_option")

        self.save()

    def delete_presence_record_label(self):
        self.delete()


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
#         verbose_name = 'Registro de Presença na lição'
#         verbose_name_plural = 'Registros de Presença nas lições'

#     def __str__(self):
#         return '{} - {} - {}'.format(self.lesson_date, self.class_id, self.user_id)
