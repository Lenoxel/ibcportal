from django.shortcuts import render
from ebd.models import EBDClass, EBDLabelOptions, EBDLesson, EBDLessonClassDetails, EBDPresenceRecord, EBDPresenceRecordLabels
from rest_framework import viewsets, status, mixins
from django.db.models import Q, F, Count, Sum, OuterRef, Subquery, Case, When
# from rest_framework.authtoken.views import ObtainAuthToken
from core.models import Post, Video, Schedule, Member, Event, MembersUnion, NotificationDevice, Church
# from ebd.models import EBDLessonPresenceRecord
from groups.models import Group
from .serializers import CustomEBDTokenObtainPairSerializer, CustomTokenObtainPairSerializer, EBDClassSerializer, EBDLabelOptionsSerializer, EBDLessonSerializer, EBDPresenceRecordLabelsSerializer, EBDPresenceRecordSerializer, PersonSerializer, PostSerializer, MemberSerializer, VideoSerializer, ScheduleSerializer, GroupSerializer, BirthdayComemorationSerializer, UnionComemorationSerializer, EventSerializer, NotificationDeviceSerializer, CongregationSerializer
from datetime import date, datetime, timedelta
# from django.contrib.auth.models import User
# from calendar import monthrange
from django.core.exceptions import ObjectDoesNotExist
# from django.utils import timezone

# from rest_framework.authtoken.models import Token
# from django.http import JsonResponse

from rest_framework.decorators import api_view, action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from core.auxiliar_functions import get_end_of_day, get_end_of_ebd_date, get_now_datetime_utc, get_start_of_day, get_sunday, get_sunday_as_date, get_today_datetime_utc

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
        Q(
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


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous or user.pk == None:
            raise NotAuthenticated({'message': 'Usuário não identificado.'})

        if user.is_superuser or user.groups.filter(name='Secretaria da Igreja').exists() or user.groups.filter(name='Superintendência').exists() or user.groups.filter(name='Admin').exists():
            class_id = self.request.query_params.get('classId', None)

            if class_id:
                students_ids = EBDClass.objects.filter(
                    pk=class_id).values_list('students', flat=True)
                teachers_ids = EBDClass.objects.filter(
                    pk=class_id).values_list('teachers', flat=True)
                secreaties_ids = EBDClass.objects.filter(
                    pk=class_id).values_list('secretaries', flat=True)

                return Member.objects.filter(
                    Q(id__in=students_ids)
                    |
                    Q(id__in=teachers_ids)
                    |
                    Q(id__in=secreaties_ids)
                ).order_by('name')

            return Member.objects.filter(
                Q(church_relation='membro')
                |
                Q(ebd_relation='aluno')
            ).order_by('name')

        member_id = Member.objects.get(user__pk=user.pk).id

        ebd_class = EBDClass.objects.filter(
            Q(teachers__id__in=[member_id])
            |
            Q(secretaries__id__in=[member_id])
        ).first()

        if not ebd_class:
            return []

        students_ids = EBDClass.objects.filter(
            pk=ebd_class.pk).values_list('students', flat=True)
        teachers_ids = EBDClass.objects.filter(
            pk=ebd_class.pk).values_list('teachers', flat=True)
        secreaties_ids = EBDClass.objects.filter(
            pk=ebd_class.pk).values_list('secretaries', flat=True)

        return Member.objects.filter(
            Q(id__in=students_ids)
            |
            Q(id__in=teachers_ids)
            |
            Q(id__in=secreaties_ids)
        ).order_by('name')

    # Cria a rota api/ebd/people/{pk}/history
    @action(detail=True, url_path='history', url_name='student_ebd_history')
    def get_student_ebd_history(self, request, pk=None):
        start_date = request.query_params.get('startDate', get_start_of_day(
            get_today_datetime_utc() - timedelta(days=90)))
        end_date = request.query_params.get(
            'endDate', get_end_of_ebd_date(get_now_datetime_utc()))

        student_presences_history = EBDPresenceRecord.objects.filter(
            Q(person__pk=pk)
            &
            Q(
                Q(lesson__date__gte=start_date),
                Q(lesson__date__lte=end_date)
            )
        ).values('attended', 'justification', 'register_on', 'register_by', student_name=F('person__name'), class_name=F('ebd_class__name'), lesson_title=F('lesson__title'), lesson_date=F('lesson__date')).order_by('-lesson__date').distinct('lesson__date')

        return Response(student_presences_history)


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


@api_view(['GET', 'POST'])
def device(request, format=None):
    if request.method == 'GET':
        devices = NotificationDevice.objects.all()
        serializer = NotificationDeviceSerializer(devices, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        new_device_id = request.data.get('device_id')
        possible_registered_device = NotificationDevice.objects.filter(
            device_id=new_device_id).values_list('device_id', flat=True).distinct()
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
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Superintendência').exists() or user.groups.filter(name='Superintendência').exists() or self.request.user.groups.filter(name='Secretários de classes de EBD').exists():
#                 data = EBDLessonPresenceRecord.class_id_index.query(class_id, EBDLessonPresenceRecord.lesson_date == lesson_date)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)
#         else:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Superintendência').exists():
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
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Superintendência').exists() or user.groups.filter(name='Superintendência').exists() or self.request.user.groups.filter(name='Secretários de classes de EBD').exists():
#                 data = EBDLessonPresenceRecord.query(lesson_date, EBDLessonPresenceRecord.user_id == user_id, scan_index_forward = True)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)
#         else:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Superintendência').exists():
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
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Superintendência').exists():
#                 data = EBDLessonPresenceRecord.query(lesson_date, scan_index_forward = True)
#             else:
#                 raise ValidationError({'message': 'você não tem permissão para acessar esse recurso.'}, code=403)
#         elif sundays_before_quantity:
#             if self.request.user.is_superuser or self.request.user.groups.filter(name='Secretaria da Igreja').exists() or self.request.user.groups.filter(name='Superintendência').exists():
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


class EBDClassViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = EBDClass.objects.all().order_by('name')
    serializer_class = EBDClassSerializer


class EBDLessonViewSet(viewsets.ModelViewSet):
    queryset = EBDLesson.objects.all().order_by('-date')
    serializer_class = EBDLessonSerializer

    # Cria a rota api/ebd/lessons/{pk}/classes
    @action(detail=True, url_path='classes', url_name='classes_by_lesson')
    def get_classes_by_lesson(self, request, pk=None):
        # ebd_lesson = self.get_object()
        ebd_classes = EBDPresenceRecord.objects.filter(lesson__pk=pk).values(class_id=F('ebd_class__id'), class_name=F(
            'ebd_class__name'), lesson_title=F('lesson__title'),).order_by('class_name').distinct('class_name')

        for ebd_class in ebd_classes:
            try:
                ebd_class['details'] = EBDLessonClassDetails.objects.filter(
                    lesson__pk=pk, ebd_class__pk=ebd_class['class_id']).values('visitors_quantity', 'money_raised')[0]
            except Exception:
                print(
                    'Erro em "for ebd_class in ebd_classes" de "get_classes_by_lesson"')

        return Response(ebd_classes)

    # Cria a rota api/ebd/lessons/{pk}/classes/{class_id}/details [GET, PUT]
    @action(detail=True, url_path=r'classes/(?P<class_id>\d+)/details', url_name='class_lesson_details', methods=['get', 'put'])
    def class_lesson_details(self, request, pk=None, class_id=None):
        if request.method == 'GET':
            try:
                class_lesson_details = EBDLessonClassDetails.objects.filter(
                    lesson=pk, ebd_class=class_id).values('visitors_quantity', 'money_raised')[0]
                return Response(class_lesson_details)
            except ObjectDoesNotExist:
                return Response({'message': 'Não existe detalhes dessa lição nessa classe'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            try:
                class_lesson_details = EBDLessonClassDetails.objects.get(
                    lesson=pk, ebd_class=class_id)
                class_lesson_details.save_details(request.data)
                return Response({'message': 'Detalhes da classe, na lição, atualizadas com sucesso!'})
            except ObjectDoesNotExist:
                return Response({'message': 'Não existe detalhes dessa lição nessa classe'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Método http não implementado'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    # Cria a rota api/ebd/lessons/{pk}/classes/{class_id}/presences
    @action(detail=True, url_path=r'classes/(?P<class_id>\d+)/presences', url_name='presences_by_class_and_lesson')
    def get_presences_by_class_and_lesson(self, request, pk=None, class_id=None):
        presences = EBDPresenceRecord.objects.filter(lesson__pk=pk, ebd_class__pk=class_id).values('id', 'attended', 'justification', 'register_on', 'person_id', person_name=F(
            'person__name'), person_nickname=F('person__nickname'), person_ebd_relation=F('person__ebd_relation'), lesson_title=F('lesson__title')).order_by('person__name')

        for presence in presences:
            is_teacher = len(list(EBDClass.objects.filter(pk=class_id, teachers__id__in=[
                             presence.get('person_id')]).values('id'))) > 0
            is_secretary = len(list(EBDClass.objects.filter(
                pk=class_id, secretaries__id__in=[presence.get('person_id')]).values('id'))) > 0
            presence['is_teacher'] = is_teacher
            presence['is_secretary'] = is_secretary

            labels = EBDPresenceRecordLabels.objects.filter(ebd_presence_record__id=presence.get('id')).values(label_id=F(
                'ebd_label_option__id'), label_title=F('ebd_label_option__title'), label_type=F('ebd_label_option__type'))
            presence['labels'] = labels
            presence['labelIds'] = map(
                lambda label: label.get('label_id'), labels)
            presence['labels_to_remove'] = []

        return Response(presences)

    # Cria a rota api/ebd/lessons/{pk}/classes/{class_id}/presences/{presence_id}
    @action(detail=True, url_path=r'classes/(?P<class_id>\d+)/presences/(?P<presence_id>\d+)', url_name='update_presence_record', methods=['put'])
    def update_presence_record(self, request, pk=None, class_id=None, presence_id=None):
        try:
            ebd_presence_record = EBDPresenceRecord.objects.get(pk=presence_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Não existe uma preseça registrada com esse id'}, status=status.HTTP_404_NOT_FOUND)

        ebd_presence_record.save_presence_record(request.data, request.user)

        for label in request.data.get('labels'):
            ebd_label_option = EBDLabelOptions.objects.get(pk=label.get('id'))

            try:
                presence_record_label = EBDPresenceRecordLabels.objects.get(
                    ebd_presence_record__id=presence_id, ebd_label_option__id=label.get('id'))
            except ObjectDoesNotExist:
                presence_record_label = EBDPresenceRecordLabels.objects.create(
                    ebd_presence_record=ebd_presence_record, ebd_label_option=ebd_label_option)

            presence_record_label.save_presence_record_label({
                'ebd_presence_record': ebd_presence_record,
                'ebd_label_option': ebd_label_option,
            })

        for label_to_remove in request.data.get('labels_to_remove'):
            try:
                presence_record_label = EBDPresenceRecordLabels.objects.get(
                    ebd_presence_record__id=presence_id, ebd_label_option__id=label_to_remove.get('id'))
                presence_record_label.delete_presence_record_label()
            except ObjectDoesNotExist:
                pass

        return Response({'message': 'Registro de presença atualizado com sucesso!'})


class EBDPresenceViewSet(viewsets.ModelViewSet):
    serializer_class = EBDPresenceRecordSerializer

    def get_queryset(self):
        # return EBDPresenceRecord.objects.all()

        return EBDPresenceRecord.objects.raw('''
            SELECT * from ebd_EBDPresenceRecord
        ''')

        # lesson_date = self.request.query_params.get('lessonDate', None)
        # classId = self.request.query_params.get('classId', None)def get_queryset
        # ).order_by('-creation_date', 'ebd_class', 'student')

        # return queryset


class EBDLabelOptionsViewSet(viewsets.ModelViewSet):
    queryset = EBDLabelOptions.objects.all().order_by('-type')
    serializer_class = EBDLabelOptionsSerializer


class EBDPresenceRecordLabelsViewSet(viewsets.ModelViewSet):
    queryset = EBDPresenceRecordLabels.objects.all().order_by(
        '-ebd_presence_record__lesson__date', 'ebd_presence_record__person__name')
    serializer_class = EBDPresenceRecordLabelsSerializer

# Equivalente a todo o card de "Números Gerais" no app


class EBDAnalyticsPresenceCountsViewSet(viewsets.ViewSet):
    def list(self, request):
        current_year = date.today().year

        lessons_count = EBDLesson.objects.filter(
            date__year=current_year).count()
        students_count = EBDPresenceRecord.objects.filter(
            register_on__year=current_year,
            attended=True
        ).count()
        visitors_count = EBDLessonClassDetails.objects.filter(
            lesson__date__year=current_year
        ).aggregate(
            total_visitors=Sum('visitors_quantity')
        )['total_visitors']

        return Response({
            'lessons_count': lessons_count or 0,
            'students_count': students_count or 0,
            'visitors_count': visitors_count or 0
        })


# Equivalente a todo o card de "Acompanhamento de Presença por Domingo" no app
class EBDAnalyticsPresenceHistoryViewSet(viewsets.ViewSet):
    def list(self, request):
        date_to_compare = get_sunday_as_date(6)

        presences = Count('attended', filter=Q(attended=True))
        absences = Count('attended', filter=Q(attended=False))

        presence_history = EBDPresenceRecord.objects.values(
            lesson_date=F('lesson__date'), lesson_title=F('lesson__title')
        ).annotate(presences=presences).annotate(absences=absences).filter(
            lesson__date__gte=date_to_compare,
            lesson__date__lte=datetime.today().date(),
        ).order_by('lesson_date')

        return Response(presence_history)

# Equivalente ao grupo de cards agrupados por classe, mostrando a quantidade de matriculados, presentes, ausentes e visitantes, em um determinado Domingo selecionado ou a média considerando todos os domingos dentro de um período de datas


class EBDAnalyticsPresenceClassesViewSet(viewsets.ViewSet):
    def list(self, request):
        start_date: str = self.request.query_params.get('startDate', None)
        end_date: str = self.request.query_params.get('endDate', None)
        month: str = self.request.query_params.get('month', None)
        day: str = self.request.query_params.get('day', None)

        filter_by_period = False

        if start_date and end_date:
            filter_by_period = True

            now = get_now_datetime_utc().date()

            start_year, start_month, start_day = start_date.split('-')
            filtered_start_date = now.replace(
                year=int(start_year), month=int(start_month), day=int(start_day))

            end_year, end_month, end_day = end_date.split('-')
            filtered_end_date = now.replace(
                year=int(end_year), month=int(end_month), day=int(end_day))
        elif day and month:
            now = get_now_datetime_utc().date()
            filtered_lesson_date = now.replace(month=int(month), day=int(day))
        else:
            filtered_lesson_date = get_sunday_as_date(0)

        # magazines = Subquery(
        #     EBDPresenceRecordLabels.objects.filter(
        #         ebd_presence_record__ebd_class__name=OuterRef('class_name'),
        #         ebd_presence_record__lesson__title=OuterRef('lesson_name'),
        #         ebd_label_option__title__icontains='trouxe revista'
        #     ).values()
        # )

        if filter_by_period:
            lessons_quantity = 0
            date_to_increment = filtered_start_date
            while date_to_increment <= filtered_end_date:
                lessons_quantity = lessons_quantity + \
                    1 if date_to_increment.weekday() == 6 else lessons_quantity
                date_to_increment = date_to_increment + timedelta(days=1)

            presences = Count(Case(When(attended=True, then=1)))
            absences = Count(Case(When(attended=False, then=1)))

            presence_classes = EBDPresenceRecord.objects.values(class_id=F('ebd_class__id'), class_name=F('ebd_class__name')).annotate(
                presences=presences, absences=absences, registered=absences + presences).filter(
                Q(
                    Q(lesson__date__range=(filtered_start_date, filtered_end_date)),
                    ~Q(ebd_class__name='Departamento Infantil')
                )
            ).order_by('class_name')

            best_frequency, best_frequency_class, worst_frequency, worst_frequency_class = 0, None, 100, None

            for presence_class in presence_classes:
                presence_class['presences'] = round(
                    presence_class['presences'] / lessons_quantity, 2)
                presence_class['absences'] = round(
                    presence_class['absences'] / lessons_quantity, 2)
                presence_class['registered'] = round(
                    presence_class['registered'] / lessons_quantity, 2)

                presence_class['frequency'] = round((presence_class['presences'] * 100) / (
                    presence_class['presences'] + presence_class['absences']), 2)
                if presence_class['frequency'] > best_frequency:
                    best_frequency = presence_class['frequency']
                    best_frequency_class = presence_class['class_id']
                if presence_class['frequency'] < worst_frequency:
                    worst_frequency = presence_class['frequency']
                    worst_frequency_class = presence_class['class_id']
        else:
            presences = Count('attended', filter=Q(attended=True))
            absences = Count('attended', filter=Q(attended=False))
            visitors = Subquery(
                EBDLessonClassDetails.objects.filter(
                    ebd_class__name=OuterRef('class_name'),
                    lesson__title=OuterRef('lesson_name')
                ).values('visitors_quantity')
            )

            presence_classes = EBDPresenceRecord.objects.values(class_name=F('ebd_class__name'), class_id=F('ebd_class__id'), lesson_name=F('lesson__title'), lesson_date=F('lesson__date')).annotate(registered=absences+presences).annotate(presences=presences).annotate(absences=absences).filter(
                Q(
                    Q(lesson__date=filtered_lesson_date),
                    ~Q(ebd_class__name='Departamento Infantil')
                )
            ).annotate(visitors=visitors).order_by('class_name')

            best_frequency, best_frequency_class, worst_frequency, worst_frequency_class = 0, None, 100, None

            for presence_class in presence_classes:
                presence_class['frequency'] = round((presence_class['presences'] * 100) / (
                    presence_class['presences'] + presence_class['absences']), 2)
                if presence_class['frequency'] > best_frequency:
                    best_frequency = presence_class['frequency']
                    best_frequency_class = presence_class['class_id']
                if presence_class['frequency'] < worst_frequency:
                    worst_frequency = presence_class['frequency']
                    worst_frequency_class = presence_class['class_id']

                    presence_class['magazines'] = EBDPresenceRecordLabels.objects.filter(
                        ebd_presence_record__ebd_class__name=presence_class['class_name'],
                        ebd_presence_record__lesson__title=presence_class['lesson_name'],
                        ebd_label_option__title__icontains='trouxe revista'
                    ).count()

        return Response({
            'best_frequency_class': best_frequency_class,
            'worst_frequency_class': worst_frequency_class,
            'classes': presence_classes,
        })


class EBDAnalyticsPresenceUsersViewSet(viewsets.ViewSet):
    def list(self, request):
        presence_users = EBDPresenceRecord.objects.raw('''
            SELECT * FROM (SELECT MAX(id) id, person_id, true role_model, (CASE WHEN attended = TRUE THEN 1 END) presences, (CASE WHEN attended = FALSE THEN 1 END) absences
            FROM ebd_EBDPresenceRecord
            GROUP BY
            person_id
            ORDER BY presences DESC
            LIMIT 5) AS T
            UNION
            SELECT * FROM (SELECT MAX(id) id, person_id, false role_model, (CASE WHEN attended = TRUE THEN 1 END) presences, (CASE WHEN attended = FALSE THEN 1 END) absences
            FROM ebd_EBDPresenceRecord
            GROUP BY 
            id,
            person_id
            ORDER BY absences DESC
            LIMIT 5) AS T2
        ''')

        formatted_presence_users = []

        for data in presence_users:
            formatted_presence_users.append({
                'person_name': data.person.name,
                'person_picture_url': data.person.picture.url,
                'presences': data.presences or 0,
                'absences': data.absences or 0,
                'role_model': data.role_model
            })

        return Response(formatted_presence_users)
