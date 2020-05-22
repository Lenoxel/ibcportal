from django.contrib import admin
from .auxiliar_functions import create_audit, create_push_notification
from .models import Post, Member, PostFile, Video, Schedule, Church, Donate, Event, MembersUnion, Audit, NotificationDevice, PushNotification
from django.core.exceptions import PermissionDenied

class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [ 
        PostFileInline 
    ]

    readonly_fields = ('manager', 'views_count', 'claps_count', 'dislike_count')

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
                post_id = Post.objects.filter(title=form.cleaned_data['title']).values_list('id', flat=True)
                post_id = list(post_id)
                if len(post_id) > 0:
                    create_push_notification('post', form, post_id[0])
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
                event_id = Event.objects.filter(title=form.cleaned_data['title']).values_list('id', flat=True)
                event_id = list(event_id)
                if len(event_id) > 0:
                    create_push_notification('event', form, event_id[0])
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
                video_id = Video.objects.filter(youtube_video_code=form.cleaned_data['youtube_video_code']).values_list('id', flat=True)
                video_id = list(video_id)
                if len(video_id) > 0:
                    create_push_notification('video', form, video_id[0])
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
                meeting_id = Schedule.objects.filter(title=form.cleaned_data['title']).values_list('id', flat=True)
                meeting_id = list(meeting_id)
                if len(meeting_id) > 0:
                    create_push_notification('meeting', form, meeting_id[0])
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
    readonly_fields = ('responsible', 'changed_model', 'action_type', 'description', 'obj_name',)  

    def has_delete_permission(self, request, obj=None):
        return False

class DonateAdmin(admin.ModelAdmin):
    readonly_fields = ('donor_name', 'donor_email', 'donate_type', 'payment_option', 'payment_status', 'amount')

class NotificationDeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('device_id', 'registration_type',)

class PushNotificationAdmin(admin.ModelAdmin):
     readonly_fields = ('title', 'body', 'multicast_id', 'success_count', 'failure_count', 'push_date',)


admin.site.register(Post, PostAdmin)
admin.site.register(Member)
admin.site.register(Video, VideoAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Church)
admin.site.register(Donate)
admin.site.register(Event, EventAdmin)
admin.site.register(MembersUnion)
admin.site.register(Audit, AuditAdmin)
admin.site.register(PushNotification, PushNotificationAdmin)
admin.site.register(NotificationDevice, NotificationDeviceAdmin)
