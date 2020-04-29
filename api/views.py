from django.shortcuts import render
from rest_framework import viewsets
from django.utils import timezone
from django.db.models import Q
from core.models import Post, Video, Schedule, Member, Event
# from groups.models import Group
from .serializers import PostSerializer, MemberSerializer, VideoSerializer, ScheduleSerializer, ComemorationSerializer, EventSerializer
from datetime import datetime, timedelta
from calendar import monthrange

# Below, the ViewSets that define the view behavior - just to be called by api (app ibc).
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(Q(published_date__lte=timezone.now()) | Q(published_date__isnull=True)).order_by('-published_date')
    serializer_class = PostSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class CelebrationViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.filter(
        Q(date_of_birth__month=timezone.now().month)
    )
    serializer_class = ComemorationSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-registering_date')
    serializer_class = VideoSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    one_week_after_period = datetime.today() + timedelta(days=7)
    one_week_before_period = datetime.today() - timedelta(days=7)
    queryset = Schedule.objects.filter(
        Q(start_date__gte=one_week_before_period), 
        Q(start_date__lte=one_week_after_period)
    ).order_by('-start_date')
    serializer_class = ScheduleSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all().order_by('name')
#     serializer_class = GroupSerializer

class EventViewSet(viewsets.ModelViewSet):
    two_months_period = datetime.today() + timedelta(days=90)
    queryset = Event.objects.filter(
        Q(start_date__gte=timezone.now()), 
        Q(start_date__lte=two_months_period)
    ).order_by('-start_date')
    serializer_class = EventSerializer
