from datetime import datetime
from django.contrib import admin
from .models import EBDClass, EBDClassLesson, EBDLessonPresenceRecord
from django.core.exceptions import PermissionDenied
from django.utils import timezone

class EBDClassLessonAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # groups_values = request.user.groups.values_list('name', flat = True)
        # groups_values_as_list = list(groups_values)

        if request.user.is_superuser or request.user.groups.filter(name='Secretaria da Igreja').exists():
            super().save_model(request, obj, form, change)

            ebd_classes = [form.cleaned_data['ebd_class']] if form.cleaned_data['ebd_class'] is not None else EBDClass.objects.all()
            for ebd_class in ebd_classes:
                for student in ebd_class.students.all():
                    lesson_date = form.cleaned_data['date'].strftime('%d/%m/%Y')
                    user_id = str(student.user)
                    class_id = str(ebd_class.pk)
                    lesson_name = form.cleaned_data['title']

                    ebd_lesson_presence_record_item = EBDLessonPresenceRecord(lesson_date, user_id, class_id=class_id, lesson_name=lesson_name, created_by=str(request.user), creation_date=timezone.now())
                    ebd_lesson_presence_record_item.save()
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser or request.user.groups.filter(name='Secretaria da Igreja').exists():
            super().delete_model(request, obj)
        else:
            return PermissionDenied


admin.site.register(EBDClass)
admin.site.register(EBDClassLesson, EBDClassLessonAdmin)