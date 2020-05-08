from django.contrib import admin
from .models import Post, Member, PostFile, Video, Schedule, Church, Donate, Event, MembersUnion
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

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('interested_people_count',)

# class DonateAdmin(admin.ModelAdmin):
#     readonly_fields = ('donor_name', 'donor_email', 'donate_type', 'payment_option', 'payment_status', 'amount')

admin.site.register(Post, PostAdmin)
admin.site.register(Member)
admin.site.register(Video)
admin.site.register(Schedule)
admin.site.register(Church)
admin.site.register(Donate)
admin.site.register(Event, EventAdmin)
admin.site.register(MembersUnion)
