from django.contrib import admin
from .models import Group, GroupMeetingDate

class GroupMeetingDateInline(admin.TabularInline):
    model = GroupMeetingDate
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    inlines = [ 
        GroupMeetingDateInline 
    ]

admin.site.register(Group, GroupAdmin)
