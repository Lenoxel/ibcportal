from datetime import date, datetime
from importlib import resources
from django.contrib import admin
from .auxiliar_functions import create_audit, create_push_notification
from .models import Post, Member, PostFile, Video, Schedule, Church, Donate, Event, MembersUnion, Audit, NotificationDevice, PushNotification
from django.core.exceptions import PermissionDenied
from import_export.admin import ExportActionMixin
from import_export import resources, widgets
from import_export.fields import Field


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [
        PostFileInline
    ]

    readonly_fields = ('manager', 'views_count',
                       'claps_count', 'dislike_count')

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, 'Post', action_type, obj)
            # Salvando o model
            obj.manager = request.user
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação da postagem
            if change == False and form.cleaned_data['to_notify'] == True:
                post = Post.objects.earliest('-id')
                create_push_notification('post', form, post.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Post', "delete", obj)
            # Salvando o model
            obj.manager = request.user
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('interested_people_count',)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, 'Event', action_type, obj)
            # Salvando o model
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação do evento
            if change == False:
                event = Event.objects.earliest('-id')
                create_push_notification('event', form, event.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Event', "delete", obj)
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class VideoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, 'Video', action_type, obj)

            # Salvando o model
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação do vídeo
            if change == False:
                video = Video.objects.earliest('-id')
                create_push_notification('video', form, video.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Video', "delete", obj)
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class ScheduleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, 'Schedule', action_type, obj)
            # Salvando o model
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação do evento
            if change == False:
                meeting = Schedule.objects.earliest('-id')
                create_push_notification('meeting', form, meeting.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Schedule', "delete", obj)
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class AuditAdmin(admin.ModelAdmin):
    readonly_fields = ('responsible', 'changed_model',
                       'action_type', 'description', 'obj_name',)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False


class DonateAdmin(admin.ModelAdmin):
    readonly_fields = ('donor_name', 'donor_email', 'donate_type',
                       'payment_option', 'payment_status', 'amount')


class NotificationDeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('device_id', 'registration_type',)


class PushNotificationAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'body', 'multicast_id',
                       'success_count', 'failure_count', 'push_date',)


class CustomDateWidget(widgets.DateWidget):
    def render(self, value: date, obj=None):
        if not value:
            return ''
        return value.strftime('%d/%m/%Y')


class CustomDateTimeWidget(widgets.DateTimeWidget):
    def render(self, value: datetime, obj=None):
        if not value:
            return ''
        return value.strftime('%d/%m/%Y %H:%M')


class CustomBooleanWidget(widgets.BooleanWidget):
    def render(self, value: bool, obj=None):
        # print(value)
        return 'Sim' if value else 'Não'


class MemberResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Nome')
    nickname = Field(attribute='nickname', column_name='Conhecido como')
    date_of_birth = Field(attribute='date_of_birth',
                          column_name='Data de nascimento', widget=CustomDateWidget())
    church_relation = Field(attribute='church_relation',
                            column_name='Relação com a Igreja')
    ebd_relation = Field(attribute='ebd_relation',
                         column_name='Relação com a EBD')
    educational_level = Field(attribute='educational_level',
                              column_name='Grau de escolaridade')
    have_a_job = Field(attribute='have_a_job',
                       column_name='Trabalha atualmente', widget=CustomBooleanWidget())
    is_retired = Field(attribute='is_retired',
                       column_name='É aposentado', widget=CustomBooleanWidget())
    work_on_sundays = Field(attribute='work_on_sundays',
                            column_name='Trabalha aos domingos', widget=CustomBooleanWidget())
    last_updated_date = Field(attribute='last_updated_date',
                              column_name='Última atualização', widget=CustomDateTimeWidget())

    class Meta:
        model = Member
        skip_unchanged = True
        report_skipped = False
        fields = ('name', 'nickname', 'date_of_birth',
                  'church_relation', 'ebd_relation', 'educational_level', 'have_a_job', 'is_retired', 'work_on_sundays', 'last_updated_date')


class MemberAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = MemberResource
    list_filter = ('name', 'church_relation',
                   'ebd_relation', 'marital_status', 'educational_level', 'have_a_job', 'is_retired', 'work_on_sundays')
    readonly_fields = ['preview_da_foto']


admin.site.register(Post, PostAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Church)
admin.site.register(Donate)
admin.site.register(Event, EventAdmin)
admin.site.register(MembersUnion)
admin.site.register(Audit, AuditAdmin)
admin.site.register(PushNotification, PushNotificationAdmin)
admin.site.register(NotificationDevice, NotificationDeviceAdmin)
