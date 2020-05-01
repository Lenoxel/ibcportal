from django.contrib import admin
from .models import Post, PostReaction, Member, PostFile, PostView, Video, VideoReaction, VideoView, Schedule, Church, Donate, Event
from django.core.exceptions import PermissionDenied

class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [ 
        PostFileInline 
    ]

    readonly_fields = ('manager',)

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

admin.site.register(Post, PostAdmin)
admin.site.register(PostReaction)
admin.site.register(Member)
admin.site.register(PostView)
admin.site.register(Video)
admin.site.register(VideoReaction)
admin.site.register(Schedule)
admin.site.register(Church)
admin.site.register(Donate)
admin.site.register(Event)
admin.site.register(VideoView)
