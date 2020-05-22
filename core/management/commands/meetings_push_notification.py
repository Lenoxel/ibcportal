from django.core.management.base import BaseCommand, CommandError
from core.models import Schedule
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from core.models import NotificationDevice, PushNotification
from pyfcm import FCMNotification
from core.auxiliar_functions import meeting_types

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            meetings = Schedule.objects.filter(
                Q(start_date__day=datetime.now().day)
            ).values_list('title', flat=True).order_by('start_date')
            meetings = list(meetings)
        except Exception:
            raise CommandError('There are no meetings today :(')
            return

        if len(meetings) > 0:
            all_devices = NotificationDevice.objects.values_list('device_id', flat=True).distinct()
            all_devices = list(all_devices)
            
            if len(all_devices) > 0:
                push_service = FCMNotification(api_key=settings.FIREBASE_KEY)

                registration_ids = all_devices

                valid_registration_ids = push_service.clean_registration_ids(registration_ids)

                if len(valid_registration_ids) > 0:
                    message_title = 'Psiu, hoje tem culto visse'
                    if len(meetings) == 1:
                        message_body = 'E pode ir se organizando, porque hoje vai ter ' + meeting_types.get(meetings[0].title) + ' às ' + meetings[0].start_date.strftime('%H:%M') + '.'
                    else:
                        message_body = 'E pode ir se organizando, porque hoje tem programação:'
                        for meeting in meetings:
                            message_body += '\r\n' + '- ' + meeting_types.get(meeting.title) + ' às ' + meeting.start_date.strftime('%H:%M') + '.'

                    data_message = {
                        "entity_type" : 'meeting',
                        "redirect" : True
                    }

                    result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

                    push_notification_object = {
                        'title': message_title,
                        'body': message_body,
                        'multicast_id': result.get('multicast_ids')[0],
                        'success_count': result.get('success'),
                        'failure_count': result.get('failure'),
                        'push_date': datetime.now()
                    }
                    push_notification = PushNotification()
                    # Salvando as informações do push notification no banco
                    push_notification.save_notification(push_notification_object)

                if len(registration_ids) > len(valid_registration_ids):
                    invalid_device_ids = NotificationDevice.objects.exclude(device_id__in=valid_registration_ids)
                    invalid_device_ids.delete()
                    return
                return
            return
        return