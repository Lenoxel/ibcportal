from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

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
