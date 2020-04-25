from rest_framework import serializers
from .models import Post, Member, Video, Schedule

# Serializers define the API representation.
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','publisher', 'title', 'text', 'published_date', 'last_updated_date')

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'description', 'address', 'date_of_birth')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'src', 'category', 'title', 'description', 'registering_date')

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'title', 'start_date', 'end_date', 'location', 'description', 'preacher', 'organizing_group', 'category')