from django.shortcuts import render
from ebd.models import EBDPresenceRecord
from rest_framework import viewsets, status, generics
from django.db.models import Q
# from rest_framework.authtoken.views import ObtainAuthToken
from core.models import Post, Video, Schedule, Member, Event, MembersUnion, NotificationDevice, Church
# from ebd.models import EBDLessonPresenceRecord
from groups.models import Group
from .serializers import CustomEBDTokenObtainPairSerializer, CustomTokenObtainPairSerializer, EBDPresenceRecordSerializer, PostSerializer, MemberSerializer, VideoSerializer, ScheduleSerializer, GroupSerializer, BirthdayComemorationSerializer, UnionComemorationSerializer, EventSerializer, NotificationDeviceSerializer, CongregationSerializer
from datetime import timedelta
# from django.contrib.auth.models import User
# from calendar import monthrange
# from django.core.exceptions import ObjectDoesNotExist
# from django.utils import timezone

# from rest_framework.authtoken.models import Token
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from core.auxiliar_functions import get_now_datetime_utc, get_sunday, get_today_datetime_utc

# Token validator and generator
# def token_request(request):
#     try:
#         new_token = Token.objects.get_or_create(user=request.user)
#         return JsonResponse({'token': new_token[0].key}, status=status.HTTP_200_OK)
#     except Exception as message:
#         return JsonResponse({'mensagem': 'você não tem permissão.'}, status=status.HTTP_401_UNAUTHORIZED)

# Generate token for all users
# def create_auth_token(request):
#     try:
#         for user in User.objects.all():
#             Token.objects.get_or_create(user=user)
#         return JsonResponse({'mensagem': 'Todos os usuário têm um token agora'}, status=status.HTTP_200_OK)
#     except Exception as message:
#         return JsonResponse({'mensagem': 'você não tem permissão.'}, status=status.HTTP_401_UNAUTHORIZED)


# Below, the ViewSets that define the view behavior - just to be called by api (app ibc).

# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']

#         if request.query_params.get('reset_token'):
#             user_token_to_delete = Token.objects.get(user=user)
#             if (user_token_to_delete):
#                 user_token_to_delete.delete()

#         token, created = Token.objects.get_or_create(user=user)

#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email,
#             'name': (user.first_name if user.first_name else '') + (' ' if user.first_name and user.last_name else '') + (user.last_name if user.last_name else '')
#         })

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class CustomEBDTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomEBDTokenObtainPairSerializer

class PostViewSet(viewsets.ModelViewSet):
    # one_month_before_period = datetime.today() - timedelta(days=30)
    # two_weeks_before_period = datetime.today() - timedelta(days=14)

    # datetime_now = datetime.now(pytz.timezone('America/Recife')) + timedelta(minutes=8)
    datetime_now = get_now_datetime_utc() + timedelta(minutes=10)

    queryset = Post.objects.filter(
        Q (
            # Q(published_date__gte=two_weeks_before_period),
            Q(published_date__lte=datetime_now)
        )
    ).order_by('-published_date')

    # queryset = Post.objects.filter(
    #     Q (
    #         Q(published_date__gte=two_weeks_before_period),
    #         Q(published_date__lte=datetime_now)
    #     )
    #     |
    #     Q (
    #         Q(published_date__year=datetime_now.year),
    #         Q(published_date__month=datetime_now.month),
    #         Q(published_date__day=datetime_now.day),
    #         Q(published_date__hour__lte=datetime_now.hour)
    #     )
    # ).order_by('-published_date')

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
        Q(date_of_birth__month=get_now_datetime_utc().month)
    )

    serializer_class = BirthdayComemorationSerializer

class UnionCelebrationViewSet(viewsets.ModelViewSet):
    queryset = MembersUnion.objects.filter(
        Q(union_date__month=get_now_datetime_utc().month)
    )

    serializer_class = UnionComemorationSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.order_by('-registering_date')[0:10]
    serializer_class = VideoSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    one_week_after_period = get_today_datetime_utc() + timedelta(days=7)
    one_week_before_period = get_today_datetime_utc() - timedelta(days=7)
    queryset = Schedule.objects.filter(
        Q(start_date__gte=one_week_before_period),
        Q(start_date__lte=one_week_after_period)
    ).order_by('-start_date')
    serializer_class = ScheduleSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('general_category', 'name')
    serializer_class = GroupSerializer

class CongregationViewSet(viewsets.ModelViewSet):
    queryset = Church.objects.filter(is_congregation=True).order_by('name')
    serializer_class = CongregationSerializer

class EventViewSet(viewsets.ModelViewSet):
    three_months_period = get_today_datetime_utc() + timedelta(days=90)
    datetime_now = get_now_datetime_utc()
    queryset = Event.objects.filter(
        Q(
            Q(start_date__day=datetime_now.day),
            Q(start_date__month=datetime_now.month),
            Q(start_date__year=datetime_now.year),
        )
        |
        Q(
            Q(start_date__lte=datetime_now),
            Q(end_date__gte=datetime_now)
        )
        |
        Q(
            Q(start_date__gte=datetime_now),
            Q(start_date__lte=three_months_period)
        )
    ).order_by('start_date')
    serializer_class = EventSerializer

class EBDPresenceViewSet(viewsets.ModelViewSet):
    serializer_class = EBDPresenceRecordSerializer
    def get_queryset(self):
        return EBDPresenceRecord.objects.all()

        # lesson_date = self.request.query_params.get('lessonDate', None)
        # classId = self.request.query_params.get('classId', None)
        # member_id = self.request.query_params.get('memberId', None)

        # queryset = EBDPresenceRecord.objects.filter(
        #     Q(lesson__lesson_date=lesson_date)
        #     # Q(classId=classId),
        #     # Q(member_id=member_id)
        # ).order_by('-creation_date', 'ebd_class', 'student')

        # return queryset

@api_view(['GET', 'POST'])
def device(request, format=None):
    if request.method == 'GET':
        devices = NotificationDevice.objects.all()
        serializer = NotificationDeviceSerializer(devices, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        new_device_id = request.data.get('device_id')
        possible_registered_device = NotificationDevice.objects.filter(device_id=new_device_id).values_list('device_id', flat=True).distinct()
        possible_registered_device = list(possible_registered_device)

        if len(possible_registered_device) == 0:
            serializer = NotificationDeviceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

# class EBDClassPresencesView(generics.ListAPIView):
#     def get_queryset(self):
#         class_id = str(self.kwargs['class_id']) if self.kwargs['class_id'] is not None else None;
#         lesson_date = self.request.query_params.get('lessonDate', None)

#         if not class_id:
#             raise ValidationError('id da classe não informado.', code=400)
#         elif lesson_date:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Secretários de classes de EBD').exists():
#                 data = EBDLessonPresenceRecord.class_id_index.query(class_id, EBDLessonPresenceRecord.lesson_date == lesson_date)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)
#         else:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists():
#                 data = EBDLessonPresenceRecord.class_id_index.query(class_id)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)

#         return data

#     def get_serializer_class(self):
#         serializer = EBDLessonPresenceRecordSerializer
#         return serializer

# class EBDUserPresencesView(generics.ListAPIView):
#     def get_queryset(self):
#         user_id = str(self.kwargs['user_id']) if self.kwargs['user_id'] is not None else None;
#         lesson_date = self.request.query_params.get('lessonDate', None)

#         if not user_id:
#             raise ValidationError('id do usuário não informado.', code=400)
#         elif lesson_date:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Secretários de classes de EBD').exists():
#                 data = EBDLessonPresenceRecord.query(lesson_date, EBDLessonPresenceRecord.user_id == user_id, scan_index_forward = True)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)
#         else:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists():
#                 data = EBDLessonPresenceRecord.user_id_index.query(user_id, scan_index_forward = True)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)

#         return data

#     def get_serializer_class(self):
#         serializer = EBDLessonPresenceRecordSerializer
#         return serializer

# class EBDPresencesAnalyticsView(generics.ListAPIView):
#     def get_queryset(self):
#         sundays_before_quantity = self.request.query_params.get('sundaysBeforeQuantity', None)
#         lesson_date = self.request.query_params.get('lessonDate', None)

#         if lesson_date:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists():
#                 data = EBDLessonPresenceRecord.query(lesson_date, scan_index_forward = True)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)
#         elif sundays_before_quantity:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists():
#                 data = []
#                 for sundays_before in range(int(sundays_before_quantity)):
#                     sunday_before_date =  get_sunday(sundays_before)

#                     for item in EBDLessonPresenceRecord.church_lesson_date_index.query('ibcc2', EBDLessonPresenceRecord.lesson_date == get_sunday(sundays_before), scan_index_forward = True):
#                         data.append(item)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)
#         else:
#             data = []

#         return data

#     def get_serializer_class(self):
#         serializer = EBDLessonPresenceRecordSerializer
#         return serializer