from rest_framework import serializers
from core.models import Post, PostFile, Member, Video, Schedule, Event, MembersUnion
from groups.models import Group
from datetime import datetime

# Serializers define the API representation.
class FileSerializer(serializers.ModelSerializer):
    post_file = serializers.SerializerMethodField()

    def get_post_file(self, obj):
        return obj.post_file.url

    class Meta:
        model = PostFile
        fields = ('post_file', 'post')

class PostSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)

    publisher_picture = serializers.SerializerMethodField()

    def get_publisher_picture(self, obj):
        return obj.publisher.picture.url

    class Meta:
        model = Post
        fields = ('id', 'publisher', 'publisher_picture', 'title', 'text', 'published_date', 'last_updated_date', 'files', 'views_count', 'claps_count', 'dislike_count')
        depth = 1

class MemberSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return obj.picture.url

    class Meta:
        model = Member
        fields = ('name', 'description', 'church_function', 'address', 'date_of_birth', 'picture')

class BirthdayComemorationSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.SerializerMethodField()

    def get_date_of_birth(self, obj):
        day_number = obj.date_of_birth.day
        month_number = obj.date_of_birth.month
        birthday_day = '0' + str(day_number) if day_number < 10 else str(day_number)
        birthday_month = '0' + str(month_number) if month_number < 10 else str(month_number)
        birthday = birthday_day + '/' + birthday_month
        return birthday

    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return obj.picture.url

    class Meta:
        model = Member
        fields = '__all__'

class UnionComemorationSerializer(serializers.ModelSerializer):
    union_date = serializers.SerializerMethodField()

    def get_union_date(self, obj):
        day_number = obj.union_date.day
        month_number = obj.union_date.month
        union_day = '0' + str(day_number) if day_number < 10 else str(day_number)
        union_month = '0' + str(month_number) if month_number < 10 else str(month_number)
        union_date = union_day + '/' + union_month
        return union_date

    man_picture = serializers.SerializerMethodField()
    woman_picture = serializers.SerializerMethodField()

    def get_man_picture(self, obj):
        return obj.man.picture.url

    def get_woman_picture(self, obj):
        return obj.woman.picture.url

    class Meta:
        model = MembersUnion
        fields = '__all__'
        depth = 1

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'src', 'category', 'title', 'description', 'youtube_video_code', 'registering_date')

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'title', 'start_date', 'end_date', 'location', 'description', 'preacher', 'organizing_group', 'category', 'video')
        depth = 1

class GroupSerializer(serializers.ModelSerializer):
    background_image = serializers.SerializerMethodField()

    def get_background_image(self, obj):
        return obj.background_image.url

    class Meta:
        model = Group
        fields = ('name', 'description', 'leader', 'vice_leader', 'third_leader', 'background_image', 'church')
        depth = 1

class EventSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return obj.picture.url

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1