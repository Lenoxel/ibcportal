from django.core.management.base import BaseCommand, CommandError
from core.models import Member
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from core.models import NotificationDevice, PushNotification
from pyfcm import FCMNotification

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            birthdays = Member.objects.filter(
                Q(date_of_birth__month=datetime.now().month),
                Q(date_of_birth__day=datetime.now().day)
            ).values_list('nickname', flat=True).order_by('nickname')
            birthdays = list(birthdays)
        except Exception:
            raise CommandError('There are no birthdays today :(')
            return

        if len(birthdays) > 0:
            all_devices = NotificationDevice.objects.values_list('device_id', flat=True).distinct()
            all_devices = list(all_devices)
            
            if len(all_devices) > 0:
                push_service = FCMNotification(api_key=settings.FIREBASE_KEY)

                registration_ids = all_devices

                valid_registration_ids = push_service.clean_registration_ids(registration_ids)

                if len(valid_registration_ids) > 0:
                    message_title = 'Aniversariantes do dia'
                    message_body = 'Deixe o seu parabéns para'

                    for count, birthday in enumerate(birthdays):
                        if count == 0:
                            message_body += ' ' + birthday
                            if birthday[count] == birthday[-1]:
                                message_body += '.'
                        elif count == (len(birthdays)-1):
                            message_body += ' e ' + birthday + '.'
                        else:
                            message_body += ', ' + birthday

                    data_message = {
                        "entity_type" : 'birthday',
                        "redirect" : True
                    }

                    extra_notification_kwargs = {
                        'image': 'https://cdn0.iconfinder.com/data/icons/tiny-icons-1/100/tiny-08-512.png'
                    }

                    result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=message_title, message_body=message_body, data_message=data_message, extra_notification_kwargs=extra_notification_kwargs)

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