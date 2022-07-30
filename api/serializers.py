from datetime import date, timedelta
# from django.http import JsonResponse
from django.db.models import Count, F, Q
from core.auxiliar_functions import get_end_of_ebd_date, get_now_datetime_utc, get_start_of_day, get_today_datetime_utc
from ebd.models import EBDClass, EBDLabelOptions, EBDLesson, EBDPresenceRecord, EBDPresenceRecordLabels
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import Post, PostFile, Member, Video, Schedule, Event, MembersUnion, NotificationDevice, Church
from groups.models import Group, GroupMeetingDate

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
        return obj.picture.url if obj.picture else None

    class Meta:
        model = Member
        fields = ('name', 'description', 'church_function', 'address', 'date_of_birth', 'picture')

class PersonSerializer(serializers.ModelSerializer):
    ebd_class = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    frequency = serializers.SerializerMethodField()

    def get_ebd_class(self, obj):
        ebd_class = EBDClass.objects.filter(
            Q(students__id__in=[obj.pk])
            |
            Q(teachers__id__in=[obj.pk])
            |
            Q(secretaries__id__in=[obj.pk])
        ).first()
        return ebd_class.name if ebd_class is not None else None

    def get_picture(self, obj):
        return obj.picture.url if obj.picture else None

    def get_frequency(self, obj):
        start_date = get_start_of_day(get_start_of_day(get_today_datetime_utc() - timedelta(days=90)))
        end_date = get_end_of_ebd_date(get_now_datetime_utc())

        person_presence_history_list = EBDPresenceRecord.objects.filter(
            Q(person__pk=obj.pk)
            &
            Q(
                Q(lesson__date__gte=start_date),
                Q(lesson__date__lte=end_date)
            )
        ).values('attended', 'lesson__date').order_by('-lesson__date').distinct('lesson__date')

        frequency = {
            'absences_in_sequence': 0,
            'presences_in_sequence': 0
        }

        for presence in person_presence_history_list:
            if presence['attended'] and frequency['absences_in_sequence'] == 0:
                frequency['presences_in_sequence'] += 1
            if not presence['attended'] and frequency['presences_in_sequence'] == 0:
                frequency['absences_in_sequence'] += 1

        return frequency

    class Meta:
        model = Member
        fields = ('id', 'name', 'picture', 'ebd_class', 'whatsapp', 'work_on_sundays', 'absences_in_sequence')

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
        fields = ('id', 'title', 'start_date', 'end_date', 'location', 'description', 'preacher', 'leader', 'organizing_group', 'category', 'video')
        depth = 1

class GroupMeetingDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMeetingDate
        fields = ('group', 'day', 'start_date', 'end_date')

class GroupSerializer(serializers.ModelSerializer):
    meeting_dates = GroupMeetingDateSerializer(many=True, required=False)
    background_image = serializers.SerializerMethodField()
    leader_picture = serializers.SerializerMethodField()
    vice_leader_picture = serializers.SerializerMethodField()
    third_leader_picture = serializers.SerializerMethodField()
    general_category_icon = serializers.SerializerMethodField()

    def get_background_image(self, obj):
        return obj.background_image.url

    def get_general_category_icon(self, obj):
        if obj.general_category and obj.general_category.icon:
            return obj.general_category.icon.url
        else:
            return None

    def get_leader_picture(self, obj):
        if obj.leader and obj.leader.picture:
            return obj.leader.picture.url
        else:
            return None

    def get_vice_leader_picture(self, obj):
        if obj.vice_leader and obj.vice_leader.picture:
            return obj.vice_leader.picture.url
        else:
            return None

    def get_third_leader_picture(self, obj):
        if obj.third_leader and obj.third_leader.picture:
            return obj.third_leader.picture.url
        else:
            return None

    class Meta:
        model = Group
        fields = ('id', 'general_category', 'name', 'description', 'info', 'leader', 'leader_picture', 'vice_leader', 'vice_leader_picture', 'third_leader', 'third_leader_picture', 'background_image', 'church', 'meeting_dates', 'general_category_icon')
        depth = 1

class CongregationSerializer(serializers.ModelSerializer):
    background_image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    responsible_picture = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    general_category_icon = serializers.SerializerMethodField()

    def get_background_image(self, obj):
        return obj.background_image.url

    def get_name(self, obj):
        return obj.acronym

    def get_responsible_picture(self, obj):
        if obj.responsible and obj.responsible.picture:
            return obj.responsible.picture.url
        else:
            return None

    def get_info(self, obj):
        if obj.description:
            return obj.description
        else:
            return None

    def get_general_category_icon(self, obj):
        if obj.general_category and obj.general_category.icon:
            return obj.general_category.icon.url
        else:
            return None

    class Meta:
        model = Church
        fields = ('id', 'name', 'description', 'info', 'background_image', 'responsible', 'responsible_picture', 'is_congregation', 'general_category', 'general_category_icon')
        depth = 1

class EventSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return obj.picture.url

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1

class EBDLessonSerializer(serializers.ModelSerializer):
    is_next_lesson = serializers.SerializerMethodField()
    presence_records = serializers.SerializerMethodField()

    def get_is_next_lesson(self, obj):
        return True if obj.date > date.today() else False

    def get_presence_records(self, obj):
        return {
            'presents': EBDPresenceRecord.objects.filter(lesson__pk=obj.pk, register_on__isnull=False, attended = True).count(),
            'absents': EBDPresenceRecord.objects.filter(lesson__pk=obj.pk, register_on__isnull=False, attended = False).count(),
            'pending':  EBDPresenceRecord.objects.filter(lesson__pk=obj.pk, register_on__isnull=True).count(),
            'pending_calls': EBDPresenceRecord.objects.filter(lesson__pk=obj.pk, register_on__isnull=True).values(class_name=F('ebd_class__name')).annotate(count=Count('ebd_class__name', distinct=True))
        }

    class Meta:
        model = EBDLesson
        fields = '__all__'
        depth = 1

class EBDClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBDClass
        fields = ('id', 'name')

class EBDPresenceRecordSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()
    ebd_class = serializers.SerializerMethodField()
    ebd_church = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    def get_person(self, obj):
        return {
            'id': obj.person.id,
            'name': obj.person.name,
            'nickname': obj.person.nickname,
            'picture': obj.person.picture.url
        }

    def get_lesson(self, obj):
        return {
            'id': obj.lesson.id,
            'title': obj.lesson.title,
            'date': obj.lesson.date
        }

    def get_ebd_class(self, obj):
        return {
            'id': obj.ebd_class.id,
            'name': obj.ebd_class.name
        }

    def get_ebd_church(self, obj):
        return {
            'id': obj.ebd_church.id,
            'name': obj.ebd_church.name
        }

    def get_created_by(self, obj):
        return {
            'id': obj.created_by.id,
            'name': '{} {}'.format(obj.created_by.first_name, obj.created_by.last_name) if obj.created_by.first_name else ''
        }

    def get_labels(self, obj):
        return EBDPresenceRecordLabels.objects.filter(ebd_presence_record__pk=obj.pk).values('creation_date', 'last_updated_date', label=F('ebd_label_option'))

    class Meta:
        model = EBDPresenceRecord
        fields = '__all__'
        depth = 1

class EBDLabelOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBDLabelOptions
        fields = ('id', 'title', 'type')

class EBDPresenceRecordLabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBDPresenceRecordLabels
        fields = ('id', 'ebd_presence_record', 'ebd_label_option', 'creation_date', 'last_updated_date')
        depth = 1
    
class NotificationDeviceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    device_id = serializers.CharField()
    registration_type = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Device` instance, given the validated data.
        """
        return NotificationDevice.objects.create(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.pk
        token['email'] = user.email
        token['name'] = (user.first_name if user.first_name else '') + (' ' if user.first_name and user.last_name else '') + (user.last_name if user.last_name else '')

        return token

class CustomEBDTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.is_superuser or user.groups.filter(name='Secretaria da Igreja').exists() or user.groups.filter(name='Admin').exists() or len(list(EBDClass.objects.filter(teachers__user__id__in=[user.pk]).values('id'))) or len(list(EBDClass.objects.filter(secretaries__user__id__in=[user.pk]).values('id'))):
            token = super().get_token(user)

            token['user_id'] = user.pk
            token['email'] = user.email
            token['name'] = (user.first_name if user.first_name else '') + (' ' if user.first_name and user.last_name else '') + (user.last_name if user.last_name else '')
            token['groups'] = list(user.groups.all().values())
            token['is_superuser'] = user.is_superuser

            if not user.is_superuser and not user.groups.filter(name='Secretaria da Igreja').exists() and not user.groups.filter(name='Admin').exists():
                classes_as_a_teacher = list(EBDClass.objects.filter(teachers__user__id__in=[user.pk]).values('id', 'name'))
                token['classes_as_a_teacher'] = classes_as_a_teacher
                print(classes_as_a_teacher)
                classes_as_a_secretary = list(EBDClass.objects.filter(secretaries__user__id__in=[user.pk]).values('id', 'name'))
                token['classes_as_a_secretary'] = classes_as_a_secretary
                print(classes_as_a_teacher)

            return token
        else:
          raise ValidationError({'message': 'Você não tem permissão para acessar esse recurso.'}, code=403)

# class EBDLessonPresenceRecordSerializer(serializers.Serializer):
#     lesson_date = serializers.CharField()
#     user_id = serializers.CharField()
#     class_id = serializers.CharField()
#     lesson_name = serializers.CharField()
#     class_name = serializers.CharField()
#     church = serializers.CharField()
#     created_by = serializers.CharField()
#     creation_date = serializers.DateTimeField()
#     attended = serializers.BooleanField()
#     register_on = serializers.CharField()
#     register_by = serializers.CharField()