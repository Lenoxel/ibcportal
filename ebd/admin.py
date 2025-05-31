from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from import_export import fields, resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pytz


from core.auxiliar_functions import remove_person_from_old_ebd_classes
from core.models import Member

from .models import (
    EBDClass,
    EBDLabelOptions,
    EBDLesson,
    EBDLessonClassDetails,
    EBDPresenceRecord,
    EBDPresenceRecordLabels,
)


class EBDLessonResource(resources.ModelResource):
    magazine_title = Field(attribute="magazine_title", column_name="Revista")
    title = Field(attribute="title", column_name="Lição")
    date = Field(attribute="date", column_name="Data da lição")
    number = Field(attribute="number", column_name="Número da lição")
    creation_date = Field(attribute="creation_date", column_name="Criada em")
    last_updated_date = Field(
        attribute="last_updated_date", column_name="Última atualização"
    )

    class Meta:
        model = EBDLesson
        fields = (
            "magazine_title",
            "title",
            "date",
            "number",
            "creation_date",
            "last_updated_date",
        )


class EBDLessonAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = EBDLessonResource
    list_filter = ("title", "date")

    # Executa sempre que uma lição é criada ou atualizada
    def save_model(self, request, obj, form, change):
        # groups_values = request.user.groups.values_list('name', flat = True)
        # groups_values_as_list = list(groups_values)

        if (
            request.user.is_superuser
            or request.user.groups.filter(name="Secretaria da Igreja").exists()
            or request.user.groups.filter(name="Admin").exists()
            or request.user.groups.filter(name="Superintendência").exists()
        ):
            super().save_model(request, obj, form, change)

            if form.cleaned_data["single_class"]:
                return

            lesson = (
                EBDLesson.objects.get(pk=obj.pk)
                if change
                else EBDLesson.objects.earliest("-id")
            )

            ebd_classes = (
                [form.cleaned_data["ebd_class"]]
                if not form.cleaned_data["apply_to_all"]
                and form.cleaned_data["ebd_class"]
                else EBDClass.objects.filter(Q(is_active=True))
            )

            for ebd_class in ebd_classes:
                try:
                    ebd_lesson_class_details = (
                        EBDLessonClassDetails.objects.get(
                            ebd_class=ebd_class, lesson=lesson
                        )
                        if change
                        else EBDLessonClassDetails(lesson=lesson, ebd_class=ebd_class)
                    )
                except ObjectDoesNotExist:
                    ebd_lesson_class_details = EBDLessonClassDetails(
                        lesson=lesson, ebd_class=ebd_class
                    )
                finally:
                    ebd_lesson_class_details.save()

                for student in ebd_class.students.all():
                    try:
                        presence_record = EBDPresenceRecord.objects.get(
                            lesson=lesson, ebd_class=ebd_class, person=student
                        )
                    except ObjectDoesNotExist:
                        presence_record = EBDPresenceRecord()

                    ebdPresenceRecordObject = {
                        "lesson": lesson,
                        "person": student,
                        "ebd_class": ebd_class,
                        "created_by": request.user,
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

                for teacher in ebd_class.teachers.all():
                    try:
                        presence_record = EBDPresenceRecord.objects.get(
                            lesson=lesson, ebd_class=ebd_class, person=teacher
                        )
                    except ObjectDoesNotExist:
                        presence_record = EBDPresenceRecord()

                    ebdPresenceRecordObject = {
                        "lesson": lesson,
                        "person": teacher,
                        "ebd_class": ebd_class,
                        "created_by": request.user,
                    }
                    presence_record.initialize_object(ebdPresenceRecordObject)
                    presence_record.save()

                for secretary in ebd_class.secretaries.all():
                    try:
                        presence_record = EBDPresenceRecord.objects.get(
                            lesson=lesson, ebd_class=ebd_class, person=secretary
                        )
                    except ObjectDoesNotExist:
                        presence_record = EBDPresenceRecord()

                    ebdPresenceRecordObject = {
                        "lesson": lesson,
                        "person": secretary,
                        "ebd_class": ebd_class,
                        "created_by": request.user,
                    }
                    presence_record.initialize_object(ebdPresenceRecordObject)
                    presence_record.save()
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if (
            request.user.is_superuser
            or request.user.groups.filter(name="Secretaria da Igreja").exists()
            or request.user.groups.filter(name="Admin").exists()
            or request.user.groups.filter(name="Superintendência").exists()
        ):
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class EBDClassResource(resources.ModelResource):
    name = Field(attribute="name", column_name="Classe")
    church = Field(attribute="name", column_name="Igreja")
    students = fields.Field(
        attribute="students",
        widget=ManyToManyWidget(Member, field="name", separator="\n"),
        column_name="Alunos",
    )
    teachers = fields.Field(
        attribute="teachers",
        widget=ManyToManyWidget(Member, field="name", separator="\n"),
        column_name="Professores",
    )
    secretaries = fields.Field(
        attribute="secretaries",
        widget=ManyToManyWidget(Member, field="name", separator="\n"),
        column_name="Secretários",
    )

    class Meta:
        model = EBDClass
        fields = ("name", "church", "students", "teachers", "secretaries")


class EBDClassAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = EBDClassResource
    list_filter = ("name", "students", "teachers", "secretaries")

    # Executa sempre que uma classe de EBD é criada ou atualizada
    def save_model(self, request, obj, form, change):
        if (
            request.user.is_superuser
            or request.user.groups.filter(name="Secretaria da Igreja").exists()
            or request.user.groups.filter(name="Admin").exists()
            or request.user.groups.filter(name="Superintendência").exists()
        ):
            super().save_model(request, obj, form, change)

            for student in form.cleaned_data["students"]:
                remove_person_from_old_ebd_classes(student, obj.pk)

            for teacher in form.cleaned_data["teachers"]:
                remove_person_from_old_ebd_classes(teacher, obj.pk)

            for secretary in form.cleaned_data["secretaries"]:
                remove_person_from_old_ebd_classes(secretary, obj.pk)
        else:
            return PermissionDenied


class EBDLessonClassDetailsAdmin(admin.ModelAdmin):
    readonly_fields = (
        "lesson",
        "ebd_class",
        "visitors_quantity",
        "money_raised",
        "creation_date",
        "last_updated_date",
    )


class EBDPresenceRecordResource(resources.ModelResource):
    lesson = Field(attribute="lesson__title", column_name="Lição")
    person = Field(attribute="person__name", column_name="Aluno")
    ebd_class = Field(attribute="ebd_class__name", column_name="Classe")
    attended = Field(attribute="attended", column_name="Presente")
    justification = Field(
        attribute="justification", column_name="Justificativa de falta"
    )
    register_on = Field(attribute="register_on", column_name="Registro de presença em")

    class Meta:
        model = EBDPresenceRecord
        fields = (
            "lesson",
            "person",
            "ebd_class",
            "attended",
            "justification",
            "register_on",
        )


def presence_records_generate_pdf(modeladmin, request, queryset):
    lesson_id = request.GET.get("lesson__id__exact")
    lesson_info = "Presença dos Alunos"

    if lesson_id:
        lesson = EBDLesson.objects.get(id=lesson_id)
        lesson_date = lesson.date.strftime("%d/%m/%Y")
        lesson_info = f"Lição - {lesson.title}"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="chamada_ebd_{lesson_date}.pdf"'
    )

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(lesson_info, styles["Title"]))
    elements.append(Spacer(1, 12))

    headers = ["Classe", "Aluno", "Presente", "Chegada"]
    data = [headers]

    for presence_record in queryset[::-1]:
        formatted_register_on = "x"

        if presence_record.attended and presence_record.register_on:
            recife_timezone = pytz.timezone("America/Recife")
            register_on_recife_timezone = presence_record.register_on.astimezone(
                recife_timezone
            )
            formatted_register_on = register_on_recife_timezone.strftime("%H:%M")

        data.append(
            [
                presence_record.ebd_class.name,
                presence_record.person.name,
                "Sim" if presence_record.attended else "x",
                formatted_register_on,
            ]
        )

    table = Table(data)

    style = TableStyle(
        [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey,
            ),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.whitesmoke,
            ),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]
    )

    table.setStyle(style)

    elements.append(table)

    doc.build(elements)

    return response


presence_records_generate_pdf.short_description = "Exportar selecionados para PDF"


class EBDPresenceRecordAdmin(admin.ModelAdmin):
    resource_class = EBDPresenceRecordResource
    readonly_fields = (
        "lesson",
        "person",
        "ebd_class",
        "ebd_church",
        "created_by",
        "attended",
        "register_on",
        "register_by",
        "justification",
    )
    list_filter = ("lesson", "person", "ebd_class", "attended", "register_on")
    actions = [presence_records_generate_pdf]


class EBDPresenceRecordLabelsResource(resources.ModelResource):
    ebd_lesson = Field(
        attribute="ebd_presence_record__lesson__title", column_name="Lição"
    )
    ebd_class = Field(
        attribute="ebd_presence_record__ebd_class__name", column_name="Classe"
    )
    ebd_student = Field(
        attribute="ebd_presence_record__person__name", column_name="Aluno"
    )
    ebd_label_option = Field(
        attribute="ebd_label_option__title", column_name="Etiqueta"
    )

    class Meta:
        model = EBDPresenceRecordLabels
        fields = ("ebd_lesson", "ebd_class", "ebd_student", "ebd_label_option")


class EBDPresenceRecordLabelsAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = EBDPresenceRecordLabelsResource
    readonly_fields = ("ebd_presence_record", "ebd_label_option")
    list_filter = (
        "ebd_presence_record__person__name",
        "ebd_presence_record__lesson__title",
        "ebd_label_option",
    )


admin.site.register(EBDClass, EBDClassAdmin)
admin.site.register(EBDLesson, EBDLessonAdmin)
admin.site.register(EBDLessonClassDetails, EBDLessonClassDetailsAdmin)
admin.site.register(EBDPresenceRecord, EBDPresenceRecordAdmin)
admin.site.register(EBDPresenceRecordLabels, EBDPresenceRecordLabelsAdmin)
admin.site.register(EBDLabelOptions)
