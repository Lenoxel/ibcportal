from django.contrib import admin
from .auxiliar_functions import create_audit
from .models import Post, Member, PostFile, Video, Schedule, Church, Donate, Event, MembersUnion, Audit
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
            create_audit(request.user, 'Post', action_type)
            # Salvando o model
            obj.manager = request.user
            super().save_model(request, obj, form, change)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Post', "delete")
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
            create_audit(request.user, 'Event', action_type)
            # Salvando o model
            super().save_model(request, obj, form, change)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Event', "delete")
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied

class VideoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, 'Video', action_type)
            # Salvando o model
            super().save_model(request, obj, form, change)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Video', "delete")
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied

class ScheduleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, 'Schedule', action_type)
            # Salvando o model
            super().save_model(request, obj, form, change)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, 'Schedule', "delete")
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied

class AuditAdmin(admin.ModelAdmin):
    readonly_fields = ('responsible', 'changed_model', 'action_type', 'description',)  

# class DonateAdmin(admin.ModelAdmin):
#     readonly_fields = ('donor_name', 'donor_email', 'donate_type', 'payment_option', 'payment_status', 'amount')

admin.site.register(Post, PostAdmin)
admin.site.register(Member)
admin.site.register(Video, VideoAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Church)
admin.site.register(Donate)
admin.site.register(Event, EventAdmin)
admin.site.register(MembersUnion)
admin.site.register(Audit, AuditAdmin)
