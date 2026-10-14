from django.contrib import admin
from django.test import TestCase

from core.models import Member

from .admin import EBDClassMemberJoinRequestAdmin
from .models import EBDClass, EBDClassMemberJoinRequest


class EBDClassMemberJoinRequestAdminTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(name="Membro", nickname="")
        self.ebd_class = EBDClass.objects.create(name="Peniel")
        self.join_request = EBDClassMemberJoinRequest.objects.create(
            member=self.member,
            ebd_class=self.ebd_class,
            ebd_class_member_type="student",
        )
        self.model_admin = EBDClassMemberJoinRequestAdmin(
            EBDClassMemberJoinRequest, admin.site
        )

    def test_member_without_class_has_no_class_situation(self):
        self.assertEqual(
            self.model_admin.member_current_situation(self.join_request),
            "Sem classe",
        )

    def test_student_situation_includes_current_class(self):
        self.ebd_class.students.add(self.member)

        self.assertEqual(
            self.model_admin.member_current_situation(self.join_request),
            "Aluno da classe Peniel",
        )

    def test_teacher_situation_includes_current_class(self):
        self.ebd_class.teachers.add(self.member)

        self.assertEqual(
            self.model_admin.member_current_situation(self.join_request),
            "Professor da classe Peniel",
        )

    def test_visitor_situation_includes_current_class(self):
        self.ebd_class.students.add(self.member)
        self.member.ebd_relation = "visitante"
        self.member.save(update_fields=["ebd_relation"])

        self.assertEqual(
            self.model_admin.member_current_situation(self.join_request),
            "Visitante da classe Peniel",
        )

    def test_current_situation_is_readonly_when_editing_pending_request(self):
        readonly_fields = self.model_admin.get_readonly_fields(
            request=None, obj=self.join_request
        )

        self.assertIn("member_current_situation", readonly_fields)

    def test_current_situation_is_readonly_when_editing_decided_request(self):
        self.join_request.status = "approved"
        readonly_fields = self.model_admin.get_readonly_fields(
            request=None, obj=self.join_request
        )

        self.assertIn("member_current_situation", readonly_fields)
