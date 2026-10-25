from django.contrib import admin
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from core.models import Member

from .admin import EBDClassMemberJoinRequestAdmin
from .models import EBDClass, EBDClassMemberJoinRequest
from .signals import BIBLICAL_PASSWORD_WORDS


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@example.com",
)
class EBDClassMemberJoinRequestAdminTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            name="Membro", nickname="", email="membro@example.com"
        )
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
        self.member.refresh_from_db()

        self.assertEqual(
            self.model_admin.member_current_situation(self.join_request),
            "Professor da classe Peniel",
        )
        self.assertTrue(self.member.user_id)

    def test_adding_secretary_creates_user_from_member_details(self):
        self.member.name = "Gabriel Barros da Silva Lenon"
        self.member.email = "gabriel@example.com"
        self.member.save()

        self.ebd_class.secretaries.add(self.member)
        self.member.refresh_from_db()

        user = self.member.user
        self.assertEqual(user.username, "gabriel.lenon")
        self.assertEqual(user.first_name, "Gabriel")
        self.assertEqual(user.last_name, "Lenon")
        self.assertEqual(user.email, "gabriel@example.com")
        account_email = mail.outbox[0]
        self.assertEqual(account_email.to, ["gabriel@example.com"])
        self.assertIn("gabriel.lenon", account_email.body)
        password = account_email.body.split("Senha:", 1)[1].strip().split()[0]
        self.assertRegex(password, r"^[a-z]+\.[a-z]+@\d{4}$")
        first_word, second_word = password.split("@", 1)[0].split(".")
        self.assertIn(first_word, BIBLICAL_PASSWORD_WORDS)
        self.assertIn(second_word, BIBLICAL_PASSWORD_WORDS)
        self.assertTrue(user.check_password(password))
        self.assertEqual(account_email.alternatives[0][1], "text/html")

    def test_generated_username_increments_until_available(self):
        User.objects.create_user(username="gabriel.lenon")
        User.objects.create_user(username="gabriel.lenon2")
        self.member.name = "Gabriel Lenon"
        self.member.save()

        self.ebd_class.teachers.add(self.member)
        self.member.refresh_from_db()

        self.assertEqual(self.member.user.username, "gabriel.lenon3")

    def test_member_without_email_cannot_be_added_as_teacher(self):
        self.member.email = ""
        self.member.save(update_fields=["email"])

        with self.assertRaises(ValidationError):
            self.ebd_class.teachers.add(self.member)

        self.member.refresh_from_db()
        self.assertIsNone(self.member.user_id)
        self.assertEqual(mail.outbox, [])

    def test_existing_member_user_is_preserved(self):
        existing_user = User.objects.create_user(
            username="existing", first_name="Existing"
        )
        self.member.user = existing_user
        self.member.save()

        self.ebd_class.secretaries.add(self.member)

        self.assertEqual(self.member.user_id, existing_user.pk)
        self.assertEqual(User.objects.count(), 1)

    def test_adding_student_does_not_create_user(self):
        self.ebd_class.students.add(self.member)

        self.assertIsNone(self.member.user_id)

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
