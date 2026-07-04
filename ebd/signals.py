from datetime import datetime

from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.models import Member
from .models import EBDClass


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
        subject, text_content, settings.DEFAULT_FROM_EMAIL, [email]
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
        notify_membership_change(instance, "added", pk_set, "professor")
    elif action == "post_remove":
        notify_membership_change(instance, "removed", pk_set, "professor")


@receiver(m2m_changed, sender=EBDClass.secretaries.through)
def secretaries_changed(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":
        notify_membership_change(instance, "added", pk_set, "secretário")
    elif action == "post_remove":
        notify_membership_change(instance, "removed", pk_set, "secretário")
