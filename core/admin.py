from django.contrib import admin
from .models import Post, Member, PostFile, Video, Schedule, Church, Donate, Event
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
            obj.manager = request.user
            super().save_model(request, obj, form, change)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            obj.manager = request.user
            super().delete_model(request, obj)
        else:
            return PermissionDenied

class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count', 'claps_count', 'dislike_count')

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('interested_people_count',)

admin.site.register(Post, PostAdmin)
admin.site.register(Member)
admin.site.register(Video, VideoAdmin)
admin.site.register(Schedule)
admin.site.register(Church)
admin.site.register(Donate)
admin.site.register(Event, EventAdmin)
