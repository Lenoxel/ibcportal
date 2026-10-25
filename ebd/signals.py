import secrets
from collections.abc import Iterable
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.models import Member
from .models import EBDClass

BIBLICAL_PASSWORD_WORDS = (
    "ibcc2",
    "jesus",
    "cristo",
    "igreja",
    "ebd",
    "biblia",
    "oracao",
    "louvor",
    "graca",
    "paz",
    "amor",
    "luz",
    "reino",
    "ceu",
    "anjo",
    "profeta",
    "apostolo",
    "discipulo",
    "pastor",
    "ovelha",
    "salmo",
    "evangelho",
    "genesis",
    "exodo",
    "romanos",
    "corintios",
    "galatas",
    "efesios",
    "hebreus",
    "apocalipse",
    "abraao",
    "isaque",
    "jaco",
    "davi",
    "moises",
    "rute",
    "ester",
    "sara",
    "joao",
    "pedro",
    "paulo",
    "lucas",
    "mateus",
    "marcos",
    "elias",
    "noe",
    "daniel",
    "jonas",
    "samuel",
    "salomao",
    "debora",
    "josue",
    "miriam",
    "estevao",
    "jerusalem",
    "belem",
    "nazare",
    "jordao",
    "sinai",
    "jerico",
    "galileia",
    "judeia",
    "templo",
    "cruz",
    "arca",
    "alianca",
    "mana",
    "siao",
    "cana",
    "betania",
    "promessa",
    "salvacao",
    "esperanca",
    "verdade",
    "sabedoria",
    "misericordia",
    "justica",
    "adoracao",
    "bencao",
    "milagre",
    "espirito",
    "santidade",
    "caminho",
    "vida",
    "palavra",
    "cordeiro",
    "semente",
    "videira",
    "pescador",
    "deserto",
    "montanha",
    "rio",
    "fonte",
    "manancial",
    "querubim",
    "serafim",
    "jubileu",
    "pentecostes",
    "hosana",
    "amem",
    "aleluia",
    "samaritano",
    "nazareno",
    "messias",
    "emanuel",
    "tabernaculo",
    "sacrificio",
    "resgate",
    "reconciliacao",
    "pacto",
    "mandamento",
    "parabola",
    "sinal",
    "oliveira",
    "vinha",
    "figueira",
    "trigo",
    "mostarda",
    "talento",
    "denario",
    "manjedoura",
    "calvario",
    "golgota",
    "getsemani",
    "capernaum",
    "betel",
    "silo",
    "samaria",
    "tiberiades",
)


def generate_memorable_password():
    first_word = secrets.choice(BIBLICAL_PASSWORD_WORDS)
    second_word = secrets.choice(BIBLICAL_PASSWORD_WORDS)
    suffix = f"{secrets.randbelow(10000):04d}"
    return f"{first_word}.{second_word}@{suffix}"


def create_user_for_class_members(members: Iterable[Member]):
    for member in members:
        if member.user_id:
            continue

        name_parts = member.name.strip().split()
        if not name_parts:
            continue

        first_name = name_parts[0]
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        username_base = ".".join(part for part in (first_name, last_name) if part)
        username_suffix = 1

        while True:
            username = (
                username_base
                if username_suffix == 1
                else f"{username_base}{username_suffix}"
            ).lower()

            if User.objects.filter(username__iexact=username).exists():
                username_suffix += 1
                continue

            password = generate_memorable_password()
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=member.email or "",
                        password=password,
                    )
                    member.user = user
                    member.save(update_fields=["user"])

                    if member.email:
                        context = {
                            "member_name": member.name,
                            "username": username,
                            "password": password,
                            "year": datetime.now().year,
                        }

                        html_content = render_to_string(
                            "emails/account_created.html", context
                        )

                        text_content = strip_tags(html_content)

                        message = EmailMultiAlternatives(
                            "EBD: Sua conta foi criada",
                            body=text_content,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[member.email],
                            cc=["glenonsilva@gmail.com"],
                        )

                        message.attach_alternative(html_content, "text/html")
                        message.send(fail_silently=False)
            except IntegrityError:
                if User.objects.filter(username__iexact=username).exists():
                    username_suffix += 1
                    continue
                raise

            break


def get_member_email(member: Member):
    if member.email:
        return member.email
    if member.user and member.user.email:
        return member.user.email
    return None


def send_class_membership_email(
    member: Member, ebd_class: EBDClass, action: str, role_name: str
):
    email = get_member_email(member)

    if not email:
        return

    secretaries = ", ".join([s.name for s in ebd_class.secretaries.all()])

    status = f"adicionado(a) à" if action == "added" else "removido(a) da"

    subject = f"EBD: Você foi {status} classe {ebd_class.name}"

    context = {
        "member_name": member.name,
        "class_name": ebd_class.name,
        "action": action,
        "secretaries": secretaries,
        "year": datetime.now().year,
        "role_name": role_name,
    }

    html_content = render_to_string("emails/class_membership.html", context)

    text_content = strip_tags(html_content)

    message = EmailMultiAlternatives(
        subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        cc=["glenonsilva@gmail.com"],
    )
    message.attach_alternative(html_content, "text/html")
    message.send()


def notify_membership_change(instance, action, pk_set, role_name, **kwargs):
    members = Member.objects.filter(pk__in=pk_set)

    for member in members:
        send_class_membership_email(member, instance, action, role_name)


@receiver(m2m_changed, sender=EBDClass.students.through)
def students_changed(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":
        notify_membership_change(instance, "added", pk_set, "aluno")
    elif action == "post_remove":
        notify_membership_change(instance, "removed", pk_set, "aluno")


@receiver(m2m_changed, sender=EBDClass.teachers.through)
def teachers_changed(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":
        create_user_for_class_members(Member.objects.filter(pk__in=pk_set))
        notify_membership_change(instance, "added", pk_set, "professor")
    elif action == "post_remove":
        notify_membership_change(instance, "removed", pk_set, "professor")


@receiver(m2m_changed, sender=EBDClass.secretaries.through)
def secretaries_changed(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":
        create_user_for_class_members(Member.objects.filter(pk__in=pk_set))
        notify_membership_change(instance, "added", pk_set, "secretário")
    elif action == "post_remove":
        notify_membership_change(instance, "removed", pk_set, "secretário")
