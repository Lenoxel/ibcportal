import base64
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from ibcportal.settings import EMAIL_HOST_USER
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from core.models import Member
from ebd.models import EBDClass

from .serializers import MemberSerializer
from .views import MemberViewSet


class MemberSerializerTests(TestCase):
    def test_current_class_is_none_when_member_has_no_class(self):
        member = Member.objects.create(name="Sem classe", nickname="")

        data = MemberSerializer(member).data

        self.assertIsNone(data["current_class"])

    def test_current_class_includes_any_ebd_membership(self):
        member = Member.objects.create(name="Professor", nickname="")
        ebd_class = EBDClass.objects.create(name="Classe de adultos")
        ebd_class.teachers.add(member)

        data = MemberSerializer(member).data

        self.assertEqual(
            data["current_class"],
            {"id": ebd_class.id, "name": ebd_class.name},
        )


class MemberViewSetTests(TestCase):
    def test_name_filter_matches_partial_names(self):
        matching_member = Member.objects.create(name="Maria Silva", nickname="")
        Member.objects.create(name="Joao Santos", nickname="")
        request = Request(APIRequestFactory().get("/api/members/?name=maria"))
        view = MemberViewSet()
        view.request = request

        members = list(view.get_queryset())

        self.assertEqual(members, [matching_member])


@override_settings(
    GOOGLE_FORM_WEBHOOK_SECRET="test-webhook-secret",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_HOST_USER="cadastro@ibcc2.com.br",
)
class GoogleFormMemberWebhookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("google-form-member-webhook")

    def test_valid_submission_is_sent_to_member_registration_email(self):
        response = self.client.post(
            self.url,
            {"data": {"Nome": "Ana Silva", "Email": "ana@example.com"}},
            format="json",
            HTTP_X_WEBHOOK_SECRET="test-webhook-secret",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["glenonsilva@gmail.com", EMAIL_HOST_USER],
        )
        self.assertIn("Ana Silva", mail.outbox[0].body)
        self.assertIn("ana@example.com", mail.outbox[0].body)

    def test_photo_is_attached_to_email_without_creating_a_member(self):
        photo_content = b"test-image-content"
        response = self.client.post(
            self.url,
            {
                "data": {"Nome": "Ana Silva"},
                "photos": [
                    {
                        "filename": "foto.jpg",
                        "contentType": "image/jpeg",
                        "base64": base64.b64encode(photo_content).decode("ascii"),
                    }
                ],
            },
            format="json",
            HTTP_X_WEBHOOK_SECRET="test-webhook-secret",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].attachments,
            [("foto.jpg", photo_content, "image/jpeg")],
        )
        self.assertEqual(Member.objects.count(), 0)

    def test_invalid_photo_is_rejected_without_sending_email(self):
        response = self.client.post(
            self.url,
            {
                "data": {"Nome": "Ana Silva"},
                "photos": [
                    {
                        "filename": "foto.jpg",
                        "contentType": "image/jpeg",
                        "base64": "not-base64",
                    }
                ],
            },
            format="json",
            HTTP_X_WEBHOOK_SECRET="test-webhook-secret",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(mail.outbox, [])

    def test_invalid_secret_is_rejected(self):
        response = self.client.post(
            self.url,
            {"data": {"Nome": "Ana Silva"}},
            format="json",
            HTTP_X_WEBHOOK_SECRET="wrong-secret",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(mail.outbox, [])

    def test_empty_or_invalid_data_is_rejected(self):
        response = self.client.post(
            self.url,
            {"data": []},
            format="json",
            HTTP_X_WEBHOOK_SECRET="test-webhook-secret",
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.url,
            [],
            format="json",
            HTTP_X_WEBHOOK_SECRET="test-webhook-secret",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(mail.outbox, [])

    @override_settings(GOOGLE_FORM_WEBHOOK_SECRET="")
    def test_unconfigured_webhook_returns_service_unavailable(self):
        response = self.client.post(
            self.url,
            {"data": {"Nome": "Ana Silva"}},
            format="json",
            HTTP_X_WEBHOOK_SECRET="test-webhook-secret",
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(mail.outbox, [])
