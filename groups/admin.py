from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import GeneralCategory, Group, GroupMeetingDate


class GroupMeetingDateInline(TabularInline):
    model = GroupMeetingDate
    extra = 1


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    inlines = [GroupMeetingDateInline]


@admin.register(GeneralCategory)
class GeneralCategoryAdmin(ModelAdmin):
    pass
