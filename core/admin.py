from django.contrib import admin
from .models import Post, Publisher, PostFile, PostView, Video, Schedule, Group

class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [ 
        PostFileInline 
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Publisher)
admin.site.register(PostView)
admin.site.register(Video)
admin.site.register(Schedule)
admin.site.register(Group)
