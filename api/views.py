from django.shortcuts import render
from rest_framework import viewsets, status
from django.utils import timezone
from django.db.models import Q
from core.models import Post, Video, Schedule, Member, Event, MembersUnion, NotificationDevice
from groups.models import Group
from .serializers import PostSerializer, MemberSerializer, VideoSerializer, ScheduleSerializer, GroupSerializer, BirthdayComemorationSerializer, UnionComemorationSerializer, EventSerializer, NotificationDeviceSerializer
from datetime import datetime, timedelta
from calendar import monthrange

from rest_framework.authtoken.models import Token
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Toquen validator and generator
def token_request(request):
    try:
        new_token = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': new_token[0].key}, status=status.HTTP_200_OK)
    except Exception as message:
        return JsonResponse({'messagem': 'você não tem permissão.'}, status=status.HTTP_401_UNAUTHORIZED)


# Below, the ViewSets that define the view behavior - just to be called by api (app ibc).
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(Q(published_date__lte=datetime.now()) | Q(published_date__isnull=True)).order_by('-published_date')
    serializer_class = PostSerializer

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer

    def get_queryset(self):
        queryset = Member.objects.all()
        group_id = self.request.query_params.get('groupId', None)
        if group_id is not None:
            group = Group.objects.get(pk=group_id)
            queryset = group.members
        return queryset

class BirthdayCelebrationViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.filter(
        Q(date_of_birth__month=datetime.now().month)
    )
    
    serializer_class = BirthdayComemorationSerializer

class UnionCelebrationViewSet(viewsets.ModelViewSet):
    queryset = MembersUnion.objects.filter(
        Q(union_date__month=datetime.now().month)
    )

    serializer_class = UnionComemorationSerializer

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


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer

class EventViewSet(viewsets.ModelViewSet):
    three_months_period = datetime.today() + timedelta(days=90)
    queryset = Event.objects.filter(
        Q(start_date__day=datetime.now().day) 
        | 
        Q(
            Q(start_date__lte=datetime.now()), 
            Q(end_date__gte=datetime.now())
        )
        |
        Q(
            Q(start_date__gte=datetime.now()), 
            Q(start_date__lte=three_months_period)
        )
    ).order_by('start_date')
    serializer_class = EventSerializer

@api_view(['GET', 'POST'])
def device(request, format=None):
    if request.method == 'GET':
        devices = NotificationDevice.objects.all()
        serializer = NotificationDeviceSerializer(devices, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = NotificationDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
