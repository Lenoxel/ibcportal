from rest_framework import serializers
from core.models import Post, Member, Video, Schedule, Event
from groups.models import Group
from datetime import datetime

# Serializers define the API representation.
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('publisher', 'title', 'text', 'published_date', 'last_updated_date')
        depth = 1

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('name', 'description', 'church_function', 'address', 'date_of_birth', 'picture')

class ComemorationSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.SerializerMethodField()

    def get_date_of_birth(self, obj):
        day_number = obj.date_of_birth.day
        month_number = obj.date_of_birth.month
        birthday_day = '0' + str(day_number) if day_number < 10 else str(day_number)
        birthday_month = '0' + str(month_number) if month_number < 10 else str(month_number)
        birthday = birthday_day + '/' + birthday_month
        return birthday

    class Meta:
        model = Member
        fields = ('name', 'nickname', 'date_of_birth', 'picture')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('src', 'category', 'title', 'description', 'registering_date')

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('title', 'start_date', 'end_date', 'location', 'description', 'preacher', 'organizing_group', 'category')
        depth = 1

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'description', 'leader', 'vice_leader', 'third_leader', 'background_image', 'church')
        depth = 1

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'start_date', 'end_date', 'description', 'location', 'event_type', 'price', 'preacher', 'organizing_group')
        depth = 1