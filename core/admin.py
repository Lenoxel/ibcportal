from datetime import date, datetime, timedelta

# from importlib import resources
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Exists, OuterRef
from import_export import resources, widgets
from import_export.admin import ExportActionMixin
from import_export.fields import Field

from .auxiliar_functions import create_audit, create_push_notification
from .models import (
    Audit,
    Church,
    Donate,
    Event,
    Member,
    MembersUnion,
    NotificationDevice,
    Post,
    PostFile,
    PushNotification,
    Schedule,
    Video,
)


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostFileInline]

    readonly_fields = ("manager", "views_count", "claps_count", "dislike_count")

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, "Post", action_type, obj)
            # Salvando o model
            obj.manager = request.user
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação da postagem
            if change == False and form.cleaned_data["to_notify"] == True:
                post = Post.objects.earliest("-id")
                create_push_notification("post", form, post.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, "Post", "delete", obj)
            # Salvando o model
            obj.manager = request.user
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ("interested_people_count",)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, "Event", action_type, obj)
            # Salvando o model
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação do evento
            if change == False:
                event = Event.objects.earliest("-id")
                create_push_notification("event", form, event.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, "Event", "delete", obj)
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class VideoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, "Video", action_type, obj)

            # Salvando o model
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação do vídeo
            if change == False:
                video = Video.objects.earliest("-id")
                create_push_notification("video", form, video.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, "Video", "delete", obj)
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class ScheduleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Criando auditoria
            action_type = "update" if change == True else "save"
            create_audit(request.user, "Schedule", action_type, obj)
            # Salvando o model
            super().save_model(request, obj, form, change)

            # Criando Notificação push - caso seja criação do evento
            if change == False:
                meeting = Schedule.objects.earliest("-id")
                create_push_notification("meeting", form, meeting.id)
        else:
            return PermissionDenied

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            # Criando auditoria
            create_audit(request.user, "Schedule", "delete", obj)
            # Salvando o model
            super().delete_model(request, obj)
        else:
            return PermissionDenied


class AuditAdmin(admin.ModelAdmin):
    readonly_fields = (
        "responsible",
        "changed_model",
        "action_type",
        "description",
        "obj_name",
    )

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False


class DonateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "donor_name",
        "donor_email",
        "donate_type",
        "payment_option",
        "payment_status",
        "amount",
    )


class NotificationDeviceAdmin(admin.ModelAdmin):
    readonly_fields = (
        "device_id",
        "registration_type",
    )


class PushNotificationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "title",
        "body",
        "multicast_id",
        "success_count",
        "failure_count",
        "push_date",
    )


class CustomDateWidget(widgets.DateWidget):
    def render(self, value: date, obj=None):
        if not value:
            return ""
        return value.strftime("%d/%m/%Y")


class CustomDateTimeWidget(widgets.DateTimeWidget):
    def render(self, value: datetime, obj=None):
        if not value:
            return ""
        return value.strftime("%d/%m/%Y %H:%M")


class CustomBooleanWidget(widgets.BooleanWidget):
    def render(self, value: bool, obj=None):
        # print(value)
        return "Sim" if value else "Não"


class MemberResource(resources.ModelResource):
    name = Field(attribute="name", column_name="Nome")
    nickname = Field(attribute="nickname", column_name="Conhecido como")
    date_of_birth = Field(
        attribute="date_of_birth",
        column_name="Data de nascimento",
        widget=CustomDateWidget(),
    )
    church_relation = Field(
        attribute="church_relation", column_name="Relação com a Igreja"
    )
    ebd_relation = Field(attribute="ebd_relation", column_name="Relação com a EBD")
    educational_level = Field(
        attribute="educational_level", column_name="Grau de escolaridade"
    )
    have_a_job = Field(
        attribute="have_a_job",
        column_name="Trabalha atualmente?",
        widget=CustomBooleanWidget(),
    )
    is_retired = Field(
        attribute="is_retired",
        column_name="É aposentado?",
        widget=CustomBooleanWidget(),
    )
    work_on_sundays = Field(
        attribute="work_on_sundays",
        column_name="Trabalha aos domingos?",
        widget=CustomBooleanWidget(),
    )
    last_updated_date = Field(
        attribute="last_updated_date",
        column_name="Última atualização",
        widget=CustomDateTimeWidget(),
    )

    class Meta:
        model = Member
        skip_unchanged = True
        report_skipped = False
        fields = (
            "name",
            "nickname",
            "date_of_birth",
            "church_relation",
            "ebd_relation",
            "educational_level",
            "have_a_job",
            "is_retired",
            "work_on_sundays",
            "last_updated_date",
        )


class MembersUnionInlineForPersonOne(admin.StackedInline):
    model = MembersUnion
    extra = 1
    verbose_name_plural = "Relacionamento"
    fk_name = "person_one"


class MembersUnionInlineForPersonTwo(admin.StackedInline):
    model = MembersUnion
    extra = 1
    verbose_name_plural = "Relacionamento"
    fk_name = "person_two"


class HasBirthdayFilter(admin.SimpleListFilter):
    title = "Data de Aniversário cadastrada?"
    parameter_name = "has_birthday"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Sim"),
            ("no", "Não"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(date_of_birth__isnull=True)
        if self.value() == "no":
            return queryset.filter(date_of_birth__isnull=True)
        return queryset


class HasWeddingDateFilter(admin.SimpleListFilter):
    title = "Data de Casamento cadastrada?"
    parameter_name = "has_wedding_date"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Sim"),
            ("no", "Não"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            wedding_date_exists = MembersUnion.objects.filter(
                Q(person_one=OuterRef("pk")) | Q(person_two=OuterRef("pk")),
                union_date__isnull=False,
            )
            return queryset.annotate(has_wedding=Exists(wedding_date_exists)).filter(
                has_wedding=True
            )
        if self.value() == "no":
            wedding_date_is_null = MembersUnion.objects.filter(
                Q(person_one=OuterRef("pk")) | Q(person_two=OuterRef("pk")),
                union_date__year=1900,
            )
            return queryset.annotate(
                has_not_wedding=Exists(wedding_date_is_null)
            ).filter(has_not_wedding=True)
        return queryset


class HasCommemorativeDateFilter(admin.SimpleListFilter):
    title = "Data comemorativa"
    parameter_name = "commemorative_date"

    def lookups(self, request, model_admin):
        return (
            ("this_week", "Nesta semana"),
            ("this_month", "Neste mês"),
        )

    def get_commemorative_dates_this_month(self, queryset):
        today = date.today()
        month = today.month

        q_objects = (
            Q(date_of_birth__month=month)
            | Q(person_one__union_date__month=month)
            | Q(person_two__union_date__month=month)
        )

        return (
            queryset.filter(q_objects)
            .distinct()
            .order_by(
                "date_of_birth__day",
                "person_one__union_date__day",
                "person_two__union_date__day",
            )
        )

    def get_commemorative_dates_this_week(self, queryset):
        today = date.today()
        weekday = today.weekday()

        if weekday == 6:
            start = today
        else:
            start = today - timedelta(days=weekday + 1)

        end = start + timedelta(days=6)
        dates = []
        current = start

        while current <= end:
            dates.append((current.month, current.day))
            current += timedelta(days=1)

        q_objects = Q()
        for month, day in dates:
            q_objects |= Q(date_of_birth__month=month, date_of_birth__day=day)
            q_objects |= Q(
                Q(
                    person_one__union_date__month=month,
                    person_one__union_date__day=day,
                )
                | Q(
                    person_two__union_date__month=month,
                    person_two__union_date__day=day,
                )
            )

        return (
            queryset.filter(q_objects)
            .distinct()
            .order_by(
                "date_of_birth__day", "person_one__union_date", "person_two__union_date"
            )
        )

    def queryset(self, request, queryset):
        if self.value() == "this_week":
            return self.get_commemorative_dates_this_week(queryset)
        if self.value() == "this_month":
            return self.get_commemorative_dates_this_month(queryset)

        return queryset


class MemberAdmin(ExportActionMixin, admin.ModelAdmin):
    def get_inlines(self, request, obj=None):
        if obj is None:
            return [MembersUnionInlineForPersonOne]

        is_person_two = MembersUnion.objects.filter(person_two=obj).exists()

        if is_person_two:
            return [MembersUnionInlineForPersonTwo]

        return [MembersUnionInlineForPersonOne]

    inlines = []
    resource_class = MemberResource
    list_filter = (
        "name",
        HasCommemorativeDateFilter,
        HasBirthdayFilter,
        HasWeddingDateFilter,
        "church_relation",
        "ebd_relation",
        "marital_status",
        "educational_level",
        "have_a_job",
        "is_retired",
        "work_on_sundays",
    )
    readonly_fields = ["preview_da_foto"]

    def birthday_formatted(self, obj):
        if obj.date_of_birth:
            return obj.date_of_birth.strftime("%d/%m/%Y")
        return "Não informado"

    birthday_formatted.short_description = "Data de Aniversário"

    def wedding_date_formatted(self, obj):
        member_union = MembersUnion.objects.filter(
            Q(person_one=obj) | Q(person_two=obj)
        ).first()
        if member_union and member_union.union_date:
            return member_union.union_date.strftime("%d/%m/%Y")
        return "Não informado"

    wedding_date_formatted.short_description = "Data de Casamento"

    list_display = ("name", "birthday_formatted", "wedding_date_formatted")


admin.site.register(Post, PostAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Church)
admin.site.register(Donate)
admin.site.register(Event, EventAdmin)
admin.site.register(MembersUnion)
admin.site.register(Audit, AuditAdmin)
admin.site.register(PushNotification, PushNotificationAdmin)
admin.site.register(NotificationDevice, NotificationDeviceAdmin)
