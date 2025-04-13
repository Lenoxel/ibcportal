from enum import Enum

import cloudinary
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import mark_safe
from pagseguro import PagSeguro

PAYMENT_OPTION_CHOICES = [
    ("deposit", "Depósito"),
    ("pagseguro", "PagSeguro"),
    ("paypal", "Paypal"),
]

DONATE_TYPE_CHOICES = [("tithe", "Dízimo"), ("offer", "Oferta")]

STATUS_CHOICES = [
    ("pending", "Pendente"),
    ("done", "Concluído"),
    ("excluded", "Excluído"),
]


def format_string(list_or_tuple, choice):
    for data in list_or_tuple:
        if data[0] == choice:
            return data[1]


MEETING_CATEGORY_OPTIONS = [
    ("doutrina", "Culto de Doutrina"),
    ("ebd", "Escola Bíblica Dominical"),
    ("intercessao", "Culto de Intercessão"),
    ("domingo", "Culto de Domingo"),
    ("ceia", "Ceia do Senhor"),
    ("casa", "Cultuando em casa"),
    ("infantil", "Culto Infantil"),
    ("oracao", "Círculo de Oração"),
    ("domestico", "Culto doméstico"),
    ("consagracao", "Consagração"),
    ("geral", "Geral"),
]

MEMBERS_UNION_OPTIONS = [
    ("compromisso", "Compromisso"),
    ("noivado", "Noivado"),
    ("casamento", "Casamento"),
]

CHURCH_RELATION_OPTIONS = [
    ("membro", "Membro"),
    ("congregado", "Congregado"),
    ("convidado", "Convidado"),
]

EBD_RELATION_OPTIONS = [
    ("aluno", "Aluno"),
    ("visitante", "Visitante"),
]

ACTION_TYPES = [("delete", "delete"), ("update", "update"), ("create", "create")]

CHURCH_FUNCTION_OPTIONS = [
    ("corpo_diaconal", "Corpo Diaconal"),
    ("lider_de_departamento", "Líder de Grupo ou Departamento"),
    ("lideranca_de_departamento", "Liderança de Grupo ou Departamento"),
    ("pastor_principal", "Pastor Principal"),
    ("pastor_auxiliar", "Pastor Auxiliar"),
    ("professor_de_ebd", "Professor de EBD"),
    ("secretario_de_ebd", "Secretário de sala de EBD"),
    ("superintendente", "Superintendente"),
    ("membro", "Membro"),
    ("lider_de_congregacao", "Líder de Congregação"),
    ("evangelista", "Evangelista"),
]

MARITAL_STATUS_OPTIONS = [
    ("solteiro", "Solteiro (a)"),
    ("casado", "Casado (a)"),
    ("divorciado", "Divorciado (a)"),
    ("viuvo", "Viúvo (a)"),
]

EDUCATIONAL_LEVEL_OPTIONS = [
    ("educacao_infantil", "Educação infantil"),
    ("ensino_fundamental_incompleto", "Ensino fundamental incompleto"),
    ("ensino_fundamental", "Ensino fundamental"),
    ("ensino_medio_incompleto", "Ensino médio incompleto"),
    ("ensino_medio", "Ensino médio"),
    ("ensino_superior_incompleto", "Ensino superior incompleto"),
    ("ensino_superior", "Ensino superior"),
    ("pos_graduacao", "Pós-graduação"),
    ("mestrado", "Mestrado"),
    ("doutorado", "Doutorado"),
]

DEFAULT_CHURCH_ID = 1


class MeetingTypeEnum(Enum):
    PRESENCIAL = "Presencial"
    ONLINE = "Online"
    HIBRIDO = "Online e Presencial"


class Post(models.Model):
    objects = models.Manager()

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Gerenciador",
        null=True,
        on_delete=models.SET_NULL,
    )
    publisher = models.ForeignKey(
        "core.Member", verbose_name="Publicador", null=True, on_delete=models.SET_NULL
    )
    title = models.CharField("Título da postagem", max_length=200)
    text = models.TextField("Texto da postagem")
    visibility = models.CharField(
        "Visibilidade",
        choices=[("public", "Público"), ("private", "Privado")],
        max_length=10,
        default="private",
    )
    to_notify = models.BooleanField("Notificar", default=False)
    views_count = models.PositiveIntegerField("Visualizações", default=0)
    claps_count = models.PositiveIntegerField("Gostei", default=0)
    dislike_count = models.PositiveIntegerField("Não gostei", default=0)
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    published_date = models.DateTimeField("Publicado em", blank=True, null=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Postagem"
        verbose_name_plural = "Postagens"
        ordering = ["-last_updated_date"]

    def __str__(self):
        return self.title


class UserDetails(models.Model):
    user = models.OneToOneField(User, related_name="details", on_delete=models.CASCADE)
    password_changed_at = models.DateTimeField(null=True, blank=True)


class Member(models.Model):
    objects = models.Manager()

    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name="Usuário",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    name = models.CharField("Nome", max_length=200)
    nickname = models.CharField("Conhecido como", max_length=25)
    description = models.TextField("Descrição", null=True, blank=True, max_length=300)
    address = models.CharField("Endereço", null=True, blank=True, max_length=250)
    district = models.CharField("Bairro", null=True, blank=True, max_length=50)
    city = models.CharField("Cidade", null=True, blank=True, max_length=50)
    state = models.CharField("Estado", null=True, blank=True, max_length=50)
    cep = models.CharField("CEP", null=True, blank=True, max_length=10)
    date_of_birth = models.DateField("Data de nascimento", null=True, blank=True)
    marital_status = models.CharField(
        "Estado civil",
        choices=MARITAL_STATUS_OPTIONS,
        null=True,
        blank=True,
        max_length=30,
    )
    educational_level = models.CharField(
        "Grau de escolaridade",
        choices=EDUCATIONAL_LEVEL_OPTIONS,
        null=True,
        blank=True,
        max_length=50,
    )
    job_title = models.CharField("Profissão", null=True, blank=True, max_length=50)
    church_function = models.CharField(
        "Função na Igreja",
        choices=CHURCH_FUNCTION_OPTIONS,
        null=True,
        blank=True,
        max_length=50,
    )
    conversion_date = models.DateField("Data de conversão", null=True, blank=True)
    baptism_date = models.DateField("Data de batismo", null=True, blank=True)
    church_relation = models.CharField(
        "Relação com a Igreja",
        choices=CHURCH_RELATION_OPTIONS,
        max_length=20,
        null=True,
        blank=True,
    )
    ebd_relation = models.CharField(
        "Relação com a EBD",
        choices=EBD_RELATION_OPTIONS,
        max_length=20,
        null=True,
        blank=True,
    )
    have_a_job = models.BooleanField("Trabalha atualmente", default=True)
    is_retired = models.BooleanField("É aposentado", default=False)
    work_on_sundays = models.BooleanField("Trabalha aos domingos", default=False)
    children = models.ManyToManyField(
        "core.Member", related_name="filho", verbose_name="Filhos", blank=True
    )
    whatsapp = models.CharField("WhatsApp", null=True, blank=True, max_length=100)
    facebook = models.CharField("Facebook", null=True, blank=True, max_length=100)
    instagram = models.CharField("Instagram", null=True, blank=True, max_length=100)
    registration_date = models.DateField(
        "Data do cadastro", null=True, blank=True, default=timezone.now
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    # birthday = fields.BirthdayField()
    # birthday_objects = managers.BirthdayManager()

    picture = CloudinaryField("Foto", null=True, blank=True)

    def preview_da_foto(self):
        return mark_safe(
            f'<img style="border-radius: 100%;" src="{self.picture.url}" width="150" height="150" />'
        )

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ["name"]

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Member)
def member_picture_delete(sender, instance, **kwargs):
    if instance.picture and instance.picture.public_id:
        cloudinary.uploader.destroy(instance.picture.public_id)


class MembersUnion(models.Model):
    objects = models.Manager()
    person_one = models.OneToOneField(
        "core.Member",
        verbose_name="Cônjuge",
        related_name="person_one",
        on_delete=models.CASCADE,
    )
    person_two = models.OneToOneField(
        "core.Member",
        verbose_name="Cônjuge",
        related_name="person_two",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    person_two_external = models.CharField(
        "Cônjuge externo",
        max_length=100,
        null=True,
        blank=True,
    )
    union_type = models.CharField(
        "Tipo da união",
        choices=MEMBERS_UNION_OPTIONS,
        max_length=20,
        default="casamento",
    )
    union_date = models.DateField("Data da união")
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Relacionamento"
        verbose_name_plural = "Relacionamentos"
        ordering = ["-union_date"]

    def __str__(self):
        return "{} e {}".format(
            self.person_one,
            self.person_two if self.person_two else self.person_two_external,
        )


class PostFile(models.Model):
    post = models.ForeignKey(
        "core.Post",
        verbose_name="Postagem",
        on_delete=models.CASCADE,
        related_name="files",
    )
    post_file = CloudinaryField(
        "Arquivo",
        overwrite=True,
        resource_type="auto",
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        ordering = ["post_file"]


@receiver(pre_delete, sender=PostFile)
def post_file_delete(sender, instance, **kwargs):
    if instance.post_file and instance.post_file.public_id:
        cloudinary.uploader.destroy(instance.post_file.public_id)


class Video(models.Model):
    objects = models.Manager()

    src = models.CharField("URL", max_length=100, null=True)
    category = models.CharField(
        "Categoria", choices=MEETING_CATEGORY_OPTIONS, max_length=20
    )
    title = models.CharField("Título do vídeo", max_length=100)
    description = models.TextField(
        "Descrição do vídeo", max_length=800, null=True, blank=True
    )
    youtube_video_code = models.CharField(
        "Código do Youtube", max_length=150, null=True, blank=True
    )
    embed_code = models.TextField(
        "Código de incorporação do vídeo", null=True, blank=True
    )

    registering_date = models.DateTimeField("Cadastrado em", auto_now_add=True)

    class Meta:
        verbose_name = "Vídeo"
        verbose_name_plural = "Vídeos"
        ordering = ["-registering_date"]

    def __str__(self):
        return self.title


class Schedule(models.Model):
    objects = models.Manager()

    title = models.CharField(
        "Encontro", choices=MEETING_CATEGORY_OPTIONS, max_length=20
    )
    start_date = models.DateTimeField("Horário de início")
    end_date = models.DateTimeField("Horário de fim", null=True, blank=True)
    location = models.ForeignKey(
        "core.Church",
        verbose_name="Local",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=DEFAULT_CHURCH_ID,
    )
    description = models.TextField("Descrição", max_length=1000, blank=True, null=True)
    preacher = models.ForeignKey(
        "core.Member",
        verbose_name="Pregador",
        related_name="pregador",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    leader = models.ForeignKey(
        "core.Member",
        verbose_name="Dirigente",
        related_name="dirigente",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    organizing_group = models.ForeignKey(
        "groups.Group",
        verbose_name="Grupo Organizador",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    category = models.CharField(
        "Tipo",
        max_length=15,
        choices=[
            (meetingType.name, meetingType.value) for meetingType in MeetingTypeEnum
        ],
    )
    video = models.ForeignKey(
        "core.Video",
        verbose_name="Vídeo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    # does_repeat = models.BooleanField('Se repete', default=False)
    # repetition_quantity = models.IntegerField('Quantidade de repetições semanais', default=0)
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Encontro"
        verbose_name_plural = "Agenda"
        ordering = ["-start_date"]

    def __str__(self):
        if self.end_date:
            start_date = self.start_date.replace(tzinfo=timezone.utc).astimezone(
                tz=None
            )
            end_date = self.end_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            formatted_start_hour = start_date.strftime("%X")[0:5]
            formatted_end_hour = end_date.strftime("%X")[0:5]
            return "{}: {} - {} às {}".format(
                self.title,
                start_date.strftime("%x"),
                formatted_start_hour,
                formatted_end_hour,
            )
        else:
            date = self.start_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            formatted_hour = date.strftime("%X")[0:5]
            return "{}: {} - {}".format(self.title, date.strftime("%x"), formatted_hour)


class Church(models.Model):
    objects = models.Manager()

    name = models.CharField("Nome", max_length=100)
    acronym = models.CharField("Sigla", max_length=25)
    description = models.TextField("Descrição")
    address = models.CharField("Endereço", max_length=250)
    responsible = models.ForeignKey(
        "core.Member",
        verbose_name="Responsável",
        related_name="responsible",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    chief_pastor = models.ForeignKey(
        "core.Member",
        verbose_name="Pastor Principal",
        related_name="chief_pastor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    is_congregation = models.BooleanField("Congregação", default=False)
    general_category = models.ForeignKey(
        "groups.GeneralCategory",
        verbose_name="Categoria",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    background_image = CloudinaryField("Foto da Igreja")
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Igreja"
        verbose_name_plural = "Igrejas"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    objects = models.Manager()

    title = models.CharField("Evento", max_length=100)
    start_date = models.DateTimeField("Início")
    end_date = models.DateTimeField("Término")
    description = models.TextField("Descrição", max_length=1000, blank=True, null=True)
    location = models.ForeignKey(
        "core.Church",
        verbose_name="Local",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=DEFAULT_CHURCH_ID,
    )
    event_type = models.CharField("Tipo do evento", max_length=30)
    price = models.FloatField("Valor (R$)", null=True, blank=True)
    preacher = models.ForeignKey(
        "core.Member",
        verbose_name="Pregador",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    organizing_group = models.ForeignKey(
        "groups.Group",
        verbose_name="Grupo Organizador",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    picture = CloudinaryField("Imagem do evento")
    interested_people_count = models.PositiveIntegerField(
        "Pessoas Interessadas", default=0
    )
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["-start_date"]

    def __str__(self):
        start_date = self.start_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        end_date = self.end_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        formatted_start_hour = start_date.strftime("%X")[0:5]
        formatted_end_hour = end_date.strftime("%X")[0:5]
        return "{}: {} às {} - {} às {}".format(
            self.title,
            start_date.strftime("%x"),
            formatted_start_hour,
            end_date.strftime("%x"),
            formatted_end_hour,
        )


@receiver(pre_delete, sender=Event)
def event_picture_delete(sender, instance, **kwargs):
    if instance.picture and instance.picture.public_id:
        cloudinary.uploader.destroy(instance.picture.public_id)


class Audit(models.Model):
    objects = models.Manager()

    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Responsável",
        null=True,
        on_delete=models.SET_NULL,
    )
    obj_name = models.CharField("Título", max_length=150)
    changed_model = models.CharField("Modelo modificado", max_length=50)
    action_type = models.CharField("Ação", max_length=20)
    description = models.TextField("Descrição")
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)

    def create_audit(self, audit_object):
        self.responsible = audit_object.get("responsible")
        self.obj_name = audit_object.get("obj_name")
        self.changed_model = audit_object.get("changed_model")
        self.action_type = audit_object.get("action_type")
        self.description = audit_object.get("description")
        self.save()

    class Meta:
        verbose_name = "Auditoria"
        verbose_name_plural = "Auditorias"
        ordering = ["-creation_date"]

    def __str__(self):
        return '{} em "{}" ({}) feito por {} - {}'.format(
            self.action_type,
            self.obj_name,
            self.changed_model,
            self.responsible,
            self.creation_date.strftime("%d/%m/%Y %H:%M"),
        )


class Donate(models.Model):
    objects = models.Manager()

    donor_name = models.CharField("Nome", max_length=100)
    donor_email = models.EmailField("Email")
    donate_type = models.CharField(
        "Tipo de Oferta", choices=DONATE_TYPE_CHOICES, max_length=20
    )
    payment_option = models.CharField(
        "Opção de Pagamento", choices=PAYMENT_OPTION_CHOICES, max_length=20
    )
    payment_status = models.CharField(
        "Status do Pagamento", choices=STATUS_CHOICES, max_length=20, default="pending"
    )
    amount = models.FloatField("Valor")

    creation_date = models.DateTimeField("Criado em", auto_now_add=True)
    last_updated_date = models.DateTimeField("Última modificação", auto_now=True)

    class Meta:
        verbose_name = "Doação"
        verbose_name_plural = "Doações"
        ordering = ["-creation_date"]

    def __str__(self):
        donate_date = self.creation_date.replace(tzinfo=timezone.utc).astimezone(
            tz=None
        )
        return "{} de {} em {} às {}".format(
            format_string(DONATE_TYPE_CHOICES, self.donate_type),
            self.donor_name,
            donate_date.strftime("%x"),
            donate_date.strftime("%X"),
        )

    def initialize_object(self, donate_object):
        self.donor_name = donate_object.get("donor_name")
        self.donor_email = donate_object.get("donor_email")
        self.donate_type = donate_object.get("donate_Type")
        self.payment_option = donate_object.get("payment_option")
        self.amount = donate_object.get("amount")

    def pagseguro_paypal_update_status(self, status):
        if status == "3":
            self.payment_status = "done"
        elif status == "7":
            self.payment_status = "excluded"
        self.save()

    def pagseguro(self):
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL,
            token=settings.PAGSEGURO_TOKEN,
            config={"sandbox": settings.PAGSEGURO_SANDBOX},
        )

        pg.sender = {"name": self.donor_name, "email": self.donor_email}

        pg.reference_prefix = None
        pg.shipping = None
        pg.reference = self.pk

        pg.items.append(
            {
                "id": self.pk,
                "description": format_string(DONATE_TYPE_CHOICES, self.donate_type),
                "amount": "%.2f" % self.amount,
                "quantity": 1,
            },
        )

        return pg

    def paypal(self):
        paypal_dict = {
            "upload": "1",
            "business": settings.PAGSEGURO_EMAIL,
            "amount_1": "%.2f" % self.amount,
            "item_name_1": format_string(DONATE_TYPE_CHOICES, self.donate_type),
            "quantity_1": 1,
            "invoice": self.pk,
            "cmd": "_cart",
            "currency_code": "BRL",
            "charset": "utf-8",
            # "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            # "return": request.build_absolute_uri(reverse('your-return-view')),
            # "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
            # "custom": "premium_plan"
        }

        return paypal_dict


class NotificationDevice(models.Model):
    objects = models.Manager()

    device_id = models.TextField("ID do dispositivo")
    registration_type = models.CharField("Tipo do registro", max_length=100)
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)

    def save_device(self, device_object):
        self.device_id = device_object.get("device_id")
        self.registration_type = device_object.get("registration_type")
        self.save()

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        ordering = ["-creation_date"]

    def __str__(self):
        return self.device_id


class PushNotification(models.Model):
    objects = models.Manager()

    title = models.CharField("Título", max_length=60)
    body = models.CharField("Mensagem", max_length=150)
    multicast_id = models.CharField("ID único da mensagem", max_length=200)
    success_count = models.PositiveIntegerField("Mensagens enviadas")
    failure_count = models.PositiveIntegerField("Mensagens não enviadas")
    push_date = models.DateTimeField("Data do envio")
    creation_date = models.DateTimeField("Criado em", auto_now_add=True)

    def save_notification(self, notification_object):
        self.title = notification_object.get("title")
        self.body = notification_object.get("body")
        self.multicast_id = notification_object.get("multicast_id")
        self.success_count = notification_object.get("success_count")
        self.failure_count = notification_object.get("failure_count")
        self.push_date = notification_object.get("push_date")
        self.save()

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-creation_date"]

    def __str__(self):
        return "{} - Enviar em {}".format(
            self.title, self.push_date.strftime("%d/%m/%Y %H:%M")
        )
