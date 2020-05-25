from django.core.management.base import BaseCommand, CommandError
from core.models import Event
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from core.models import NotificationDevice, PushNotification
from pyfcm import FCMNotification
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            events = Event.objects.filter(
                Q(start_date__day=datetime.now().day)
            ).values_list('title', flat=True).order_by('start_date')
            events = list(events)
        except Exception:
            raise CommandError('There are no events today :(')
            return

        if len(events) > 0:
            all_devices = NotificationDevice.objects.values_list('device_id', flat=True).distinct()
            all_devices = list(all_devices)
            
            if len(all_devices) > 0:
                push_service = FCMNotification(api_key=settings.FIREBASE_KEY)

                registration_ids = all_devices

                valid_registration_ids = push_service.clean_registration_ids(registration_ids)

                if len(valid_registration_ids) > 0:
                    if len(events) == 1:
                        message_title = 'Ei! Dá uma olhada nesse evento que vai acontecer hoje'
                        message_body = 'Não perde não... Hoje vai rolar o evento "' + events[0] + '".'
                    else:
                        message_title = 'Ei! Dá uma olhada nos eventos de hoje'
                        message_body = 'Fique ligado, pois hoje teremos alguns eventos:'
                        for count, event in enumerate(events):
                            if count == 0:
                                message_body += ' "' + event + '"'
                            elif count == (len(event)-1):
                                message_body += ' e "' + event + '".'
                            else:
                                message_body += ', "' + event + '"'

                    data_message = {
                        "entity_type" : 'event',
                        "redirect" : True
                    }

                    result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

                    push_notification_object = {
                        'title': message_title,
                        'body': message_body,
                        'multicast_id': result.get('multicast_ids')[0],
                        'success_count': result.get('success'),
                        'failure_count': result.get('failure'),
                        'push_date': timezone.now()
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