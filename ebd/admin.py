from django.contrib import admin

from .models import EBDClass, EBDLabelOptions, EBDLesson, EBDPresenceRecord, EBDPresenceRecordLabels
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from import_export import resources
from import_export.admin import ExportActionMixin, ExportMixin

class EBDLessonAdmin(ExportActionMixin, admin.ModelAdmin):
    list_filter = ('title', 'date')

    def save_model(self, request, obj, form, change):
        # groups_values = request.user.groups.values_list('name', flat = True)
        # groups_values_as_list = list(groups_values)

        if request.user.is_superuser or request.user.groups.filter(name='Secretaria da Igreja').exists() or request.user.groups.filter(name='Admin').exists():
            super().save_model(request, obj, form, change)

            ebd_classes = [form.cleaned_data['ebd_class']] if form.cleaned_data['ebd_class'] is not None else EBDClass.objects.all()
            for ebd_class in ebd_classes:
                for student in ebd_class.students.all():
                    if change:
                        try:
                            presence_record = EBDPresenceRecord.objects.get(lesson__pk=obj.pk, student__pk=student.pk)
                        except ObjectDoesNotExist:
                            presence_record = EBDPresenceRecord()
                    else:
                        presence_record = EBDPresenceRecord()

                    ebdPresenceRecordObject = {
                        'lesson': EBDLesson.objects.get(pk=obj.pk) if change else EBDLesson.objects.earliest('-id'),
                        'student': student,
                        'ebd_class': ebd_class,
                        'created_by': request.user
                    }
                    presence_record.initialize_object(ebdPresenceRecordObject)
                    presence_record.save()
                       
                    # lesson_date = form.cleaned_data['date'].strftime('%d/%m/%Y')
                    # user_id = str(student.user)
                    # class_id = str(ebd_class.pk)
                    # lesson_name = form.cleaned_data['title']
                    # class_name = str(ebd_class.name)

                    # ebd_lesson_presence_record_item = EBDLessonPresenceRecord(lesson_date, user_id, class_id=class_id, lesson_name=lesson_name, class_name=class_name, church='ibcc2', created_by=str(request.user), creation_date=timezone.now())
                    # ebd_lesson_presence_record_item.save()
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser or request.user.groups.filter(name='Secretaria da Igreja').exists() or request.user.groups.filter(name='Admin').exists():
            super().delete_model(request, obj)
        else:
            return PermissionDenied

# class EBDClassResource(resources.ModelResource):
#     class Meta:
#         model = EBDClass
#         fields = ('name', 'church__name', 'students__name', 'teachers__name', 'secretaries__name')

class EBDClassAdmin(ExportActionMixin, admin.ModelAdmin):
    # resource_class = EBDClassResource
    list_filter = ('name', 'students', 'teachers', 'secretaries')

class EBDPresenceRecordAdmin(ExportActionMixin, admin.ModelAdmin):
    readonly_fields = ('lesson', 'student', 'ebd_class', 'ebd_church', 'created_by', 'attended', 'register_on') 
    list_filter = ('lesson', 'student', 'ebd_class', 'attended', 'register_on')

class EBDPresenceRecordLabelsAdmin(ExportActionMixin, admin.ModelAdmin):
    readonly_fields = ('ebd_presence_record', 'ebd_label_option') 
    list_filter = ('ebd_presence_record', 'ebd_label_option') 

admin.site.register(EBDClass, EBDClassAdmin)
admin.site.register(EBDLesson, EBDLessonAdmin)
admin.site.register(EBDPresenceRecord, EBDPresenceRecordAdmin)
admin.site.register(EBDPresenceRecordLabels, EBDPresenceRecordLabelsAdmin)
admin.site.register(EBDLabelOptions)