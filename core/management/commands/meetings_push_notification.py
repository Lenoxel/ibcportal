from datetime import datetime

import pytz
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from pyfcm import FCMNotification
from tzlocal import get_localzone

from core.auxiliar_functions import meeting_types
from core.models import NotificationDevice, PushNotification, Schedule
from groups.models import Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            now_datetime = datetime.now()
            meetings = (
                Schedule.objects.filter(
                    Q(start_date__day=now_datetime.day),
                    Q(start_date__month=now_datetime.month),
                    Q(start_date__year=now_datetime.year),
                )
                .values_list("title", "start_date", "organizing_group")
                .order_by("start_date")
            )
            meetings = list(meetings)
        except Exception:
            raise CommandError("There are no meetings today :(")
            return

        if len(meetings) > 0:
            all_devices = NotificationDevice.objects.values_list(
                "device_id", flat=True
            ).distinct()
            all_devices = list(all_devices)

            if len(all_devices) > 0:
                push_service = FCMNotification(api_key=settings.FIREBASE_KEY)

                registration_ids = all_devices

                valid_registration_ids = push_service.clean_registration_ids(
                    registration_ids
                )

                if len(valid_registration_ids) > 0:
                    local_tz = get_localzone()

                    message_title = "Psiu, hoje tem culto visse"
                    if len(meetings) == 1:
                        locale_meeting_hour = (
                            meetings[0][1].replace(tzinfo=pytz.utc).astimezone(local_tz)
                        )
                        if meetings[0][0] == "geral":
                            if meetings[0][2] is not None:
                                group = Group.objects.get(pk=meetings[0][2])
                                message_body = (
                                    "E pode ir se organizando, porque hoje vai ter programação - "
                                    + group.name
                                    + " às "
                                    + locale_meeting_hour.strftime("%H:%M")
                                    + "."
                                )
                            else:
                                message_body = (
                                    "E pode ir se organizando, porque hoje vai ter programação "
                                    + meeting_types.get(meetings[0][0])
                                    + " às "
                                    + locale_meeting_hour.strftime("%H:%M")
                                    + "."
                                )
                        else:
                            message_body = (
                                "E pode ir se organizando, porque hoje vai ter "
                                + meeting_types.get(meetings[0][0])
                                + " às "
                                + locale_meeting_hour.strftime("%H:%M")
                                + "."
                            )
                    else:
                        message_body = (
                            "E pode ir se organizando, porque hoje tem programação:\r\n"
                        )
                        for meeting in meetings:
                            locale_meeting_hour = (
                                meeting[1].replace(tzinfo=pytz.utc).astimezone(local_tz)
                            )
                            if meeting[0] == "geral":
                                if meeting[2] is not None:
                                    group = Group.objects.get(pk=meetings[0][2])
                                    message_body += (
                                        "\r\n"
                                        + "- Programação: "
                                        + group.name
                                        + " às "
                                        + locale_meeting_hour.strftime("%H:%M")
                                        + "."
                                    )
                                else:
                                    message_body += (
                                        "\r\n"
                                        + "- Programação "
                                        + meeting_types.get(meeting[0])
                                        + " às "
                                        + locale_meeting_hour.strftime("%H:%M")
                                        + "."
                                    )
                            else:
                                message_body += (
                                    "\r\n"
                                    + "- "
                                    + meeting_types.get(meeting[0])
                                    + " às "
                                    + locale_meeting_hour.strftime("%H:%M")
                                    + "."
                                )

                    data_message = {"entity_type": "meeting", "redirect": True}

                    result = push_service.notify_multiple_devices(
                        registration_ids=valid_registration_ids,
                        message_title=message_title,
                        message_body=message_body,
                        data_message=data_message,
                    )

                    push_notification_object = {
                        "title": message_title,
                        "body": message_body,
                        "multicast_id": result.get("multicast_ids")[0],
                        "success_count": result.get("success"),
                        "failure_count": result.get("failure"),
                        "push_date": timezone.now(),
                    }
                    push_notification = PushNotification()
                    # Salvando as informações do push notification no banco
                    push_notification.save_notification(push_notification_object)

                if len(registration_ids) > len(valid_registration_ids):
                    invalid_device_ids = NotificationDevice.objects.exclude(
                        device_id__in=valid_registration_ids
                    )
                    invalid_device_ids.delete()
                    return
                return
            return
        return
