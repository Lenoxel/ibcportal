from django.conf import settings
from django.db import models
from django.utils import timezone
from enum import Enum
from pagseguro import PagSeguro
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
import cloudinary
from django.dispatch import receiver


PAYMENT_OPTION_CHOICES = [
    ('deposit', 'Depósito'),
    ('pagseguro', 'PagSeguro'),
    ('paypal', 'Paypal')
]

DONATE_TYPE_CHOICES = [
    ('tithe', 'Dízimo'),
    ('offer', 'Oferta')
]

STATUS_CHOICES = [
    ('pending', 'Pendente'),
    ('done', 'Concluído'),
    ('excluded', 'Excluído')
]

def format_string(list_or_tuple, choice):
    for data in list_or_tuple:
        if data[0] == choice:
            return data[1]

MEETING_CATEGORY_OPTIONS = [
    ('doutrina', 'Culto de Doutrina'),
    ('ebd', 'Escola Bíblica Dominical'),
    ('intercessao', 'Culto de Intercessão'),
    ('domingo', 'Culto de Domingo'),
    ('ceia', 'Ceia do Senhor'),
    ('casa', 'Cultuando em casa'),
    ('infantil', 'Culto Infantil'),
    ('oracao', 'Ciclo de Oração'),
    ('domestico', 'Culto doméstico'),
    ('geral', 'Geral')
]

MEMBERS_UNION_OPTIONS = [
    ('compromisso', 'Compromisso'),
    ('noivado', 'Noivado'),
    ('casamento', 'Casamento'),
]

ACTION_TYPES = [
    ('delete', 'delete'),
    ('update', 'update'),
    ('create', 'create')
]

class MeetingTypeEnum(Enum): 
    PRESENCIAL = "Presencial"
    ONLINE = "Online"

class Post(models.Model):
    objects = models.Manager()

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Gerenciador', null=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey('core.Member', verbose_name='Publicador', null=True, on_delete=models.SET_NULL)
    title = models.CharField('Título da postagem', max_length=200)
    text = models.TextField('Texto da postagem')
    to_notify = models.BooleanField('Notificar', default=False)
    views_count = models.PositiveIntegerField('Visualizações', default=0)
    claps_count = models.PositiveIntegerField('Gostei', default=0)
    dislike_count = models.PositiveIntegerField('Não gostei', default=0)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    published_date = models.DateTimeField('Publicado em', blank=True, null=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'
        ordering = ['-last_updated_date']

    def __str__(self):
        return self.title

class Member(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    nickname = models.CharField('Conhecido como', max_length=25)
    description = models.TextField('Descrição', max_length=300)
    address = models.CharField('Endereço', max_length=100)
    church_function = models.CharField('Função na Igreja', max_length=40)
    date_of_birth = models.DateField('Data de nascimento', null=True, blank=True)
    picture = CloudinaryField('Foto')
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    # birthday = fields.BirthdayField()
    # birthday_objects = managers.BirthdayManager()

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'membros'
        ordering = ['name']

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Member)
def member_picture_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.picture.public_id)

class MembersUnion(models.Model):
    objects = models.Manager()

    man = models.OneToOneField('core.Member', verbose_name='Homem', related_name='man', on_delete=models.CASCADE)
    woman = models.OneToOneField('core.Member', verbose_name='Mulher', related_name='woman', on_delete=models.CASCADE)
    union_type = models.CharField('Tipo da união', choices=MEMBERS_UNION_OPTIONS, max_length=20)
    union_date = models.DateTimeField('Data da união')
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'União'
        verbose_name_plural = 'Uniões'
        ordering = ['-union_date']

    def __str__(self):
        return '{} e {}'.format(self.man, self.woman)

class PostFile(models.Model):
    post = models.ForeignKey('core.Post', verbose_name='Postagem', on_delete=models.CASCADE, related_name='files')
    post_file = CloudinaryField(
        'Arquivo',
        overwrite=True,
        resource_type="auto",
    )
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'
        ordering = ['post_file']

@receiver(pre_delete, sender=PostFile)
def post_file_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.post_file.public_id)

class Video(models.Model):
    objects = models.Manager()

    src = models.CharField('URL', max_length=100, blank=True)
    category = models.CharField('Categoria', choices=MEETING_CATEGORY_OPTIONS, max_length=20)
    title = models.CharField('Título do vídeo', max_length=100)
    description = models.TextField('Descrição do vídeo', max_length=800, null = True, blank = True)
    youtube_video_code = models.CharField('Código do Youtube', max_length=150, blank=True)

    registering_date = models.DateTimeField('Cadastrado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Vídeo'
        verbose_name_plural = 'Vídeos'
        ordering = ['-registering_date']

    def __str__(self):
        return self.title

class Schedule(models.Model):
    objects = models.Manager()

    title = models.CharField('Encontro', choices=MEETING_CATEGORY_OPTIONS, max_length=20)
    start_date = models.DateTimeField('Horário de início')
    end_date = models.DateTimeField('Horário de fim', null=True, blank=True)
    location = models.ForeignKey('core.Church', verbose_name='Local', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField('Descrição', max_length=1000, blank=True, null=True)
    preacher = models.ForeignKey('core.Member', verbose_name='Pregador', related_name='pregador', blank=True, null=True, on_delete=models.SET_NULL)
    leader = models.ForeignKey('core.Member', verbose_name='Dirigente', related_name='dirigente', blank=True, null=True, on_delete=models.SET_NULL)
    organizing_group = models.ForeignKey('groups.Group', verbose_name='Grupo Organizador', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.CharField('Tipo', max_length=15, choices=[(meetingType.name, meetingType.value) for meetingType in MeetingTypeEnum])
    video = models.ForeignKey('core.Video', verbose_name='Vídeo', null=True, blank=True, on_delete=models.SET_NULL)
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

class Church(models.Model):
    objects = models.Manager()

    name = models.CharField('Nome', max_length=100)
    acronym = models.CharField('Sigla', max_length=15)
    description = models.TextField('Descrição')
    address = models.CharField('Endereço', max_length=250)
    chief_pastor = models.ForeignKey('core.Member', verbose_name='Pastor Principal', null=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Igreja'
        verbose_name_plural = 'Igrejas'
        ordering = ['name']

    def __str__(self):
        return self.name

class Event(models.Model):
    objects = models.Manager()
    
    title = models.CharField('Evento', max_length=100)
    start_date = models.DateTimeField('Início')
    end_date = models.DateTimeField('Término')
    description = models.TextField('Descrição', max_length=1000, blank=True, null=True)
    location = models.ForeignKey('core.Church', verbose_name='Local', null=True, blank=True, on_delete=models.SET_NULL)
    event_type =  models.CharField('Tipo do evento', max_length=30)
    price = models.FloatField('Valor (R$)', null=True, blank=True)
    preacher = models.ForeignKey('core.Member', verbose_name='Pregador', null=True, blank=True, on_delete=models.SET_NULL)
    organizing_group = models.ForeignKey('groups.Group', verbose_name='Grupo Organizador', null=True, blank=True, on_delete=models.SET_NULL)
    picture = CloudinaryField('Imagem do evento')
    interested_people_count = models.PositiveIntegerField('Pessoas Interessadas', default=0)
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-start_date']

    def __str__(self):
        start_date = self.start_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        end_date = self.end_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        formatted_start_hour = start_date.strftime("%X")[0:5]
        formatted_end_hour = end_date.strftime("%X")[0:5]
        return '{}: {} às {} - {} às {}'.format(self.title, start_date.strftime("%x"), formatted_start_hour, end_date.strftime("%x"), formatted_end_hour)

@receiver(pre_delete, sender=Event)
def event_picture_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.picture.public_id)

class Audit(models.Model):
    objects = models.Manager()

    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Responsável', null=True, on_delete=models.SET_NULL)
    obj_name = models.CharField('Título', max_length=150)
    changed_model = models.CharField('Modelo modificado', max_length=50)
    action_type = models.CharField('Ação', max_length=20)
    description = models.TextField('Descrição')
    creation_date = models.DateTimeField('Criado em', auto_now_add=True)

    def create_audit(self, audit_object):
        self.responsible = audit_object.get('responsible')
        self.obj_name = audit_object.get('obj_name')
        self.changed_model = audit_object.get('changed_model')
        self.action_type = audit_object.get('action_type')
        self.description = audit_object.get('description')
        self.save()

    class Meta:
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'
        ordering = ['-creation_date']

    def __str__(self):
       return '{} em "{}" ({}) feito por {} - {}'.format(self.action_type, self.obj_name, self.changed_model, self.responsible, self.creation_date)

class Donate(models.Model):
    objects = models.Manager()

    donor_name = models.CharField('Nome', max_length=100)
    donor_email = models.EmailField('Email')
    donate_type = models.CharField(
        'Tipo de Oferta', choices=DONATE_TYPE_CHOICES, max_length=20
    )
    payment_option = models.CharField(
        'Opção de Pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20
    )
    payment_status = models.CharField(
        'Status do Pagamento', choices=STATUS_CHOICES, max_length=20, default='pending'
    )
    amount = models.FloatField('Valor')

    creation_date = models.DateTimeField('Criado em', auto_now_add=True)
    last_updated_date = models.DateTimeField('Última modificação', auto_now=True)

    class Meta:
        verbose_name = 'Doação'
        verbose_name_plural = 'Doações'
        ordering = ['-creation_date']

    def __str__(self):
        donate_date = self.creation_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return '{} de {} em {} às {}'.format(format_string(DONATE_TYPE_CHOICES, self.donate_type), self.donor_name, donate_date.strftime("%x"), donate_date.strftime("%X"))

    def initialize_object(self, donate_object):
        self.donor_name = donate_object.get('donor_name')
        self.donor_email = donate_object.get('donor_email')
        self.donate_type = donate_object.get('donate_Type')
        self.payment_option = donate_object.get('payment_option')
        self.amount = donate_object.get('amount')

    def pagseguro_paypal_update_status(self, status):
        if status == '3':
            self.payment_status = 'done'
        elif status == '7':
            self.payment_status = 'excluded'
        self.save()

    def pagseguro(self):
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, 
            token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )

        pg.sender = {
            'name': self.donor_name,
            'email': self.donor_email
        }
        
        pg.reference_prefix = None
        pg.shipping = None
        pg.reference = self.pk

        pg.items.append(
            {
                "id": self.pk, 
                "description": format_string(DONATE_TYPE_CHOICES, self.donate_type), 
                "amount": '%.2f' % self.amount, 
                "quantity": 1
            },
        )

        return pg
    
    def paypal(self):
        paypal_dict = {
            'upload': '1',
            'business': settings.PAGSEGURO_EMAIL,
            'amount_1': '%.2f' % self.amount,
            'item_name_1': format_string(DONATE_TYPE_CHOICES, self.donate_type),
            'quantity_1': 1,
            'invoice': self.pk,
            'cmd': '_cart',
            'currency_code': 'BRL',
            'charset': 'utf-8'
            # "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            # "return": request.build_absolute_uri(reverse('your-return-view')),
            # "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
            # "custom": "premium_plan"
        }
        
        return paypal_dict