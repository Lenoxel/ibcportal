import requests
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from tzlocal import get_localzone
from .models import Audit, NotificationDevice, PushNotification
from pyfcm import FCMNotification

meeting_types = {
    'doutrina': 'Culto de Doutrina',
    'ebd': 'Escola B. Dominical',
    'intercessao': 'Culto de Intercessão',
    'domingo': 'Culto de Domingo',
    'ceia': 'Ceia do Senhor',
    'casa': 'Cultuando em casa',
    'infantil': 'Culto Infantil',
    'oracao': 'Círculo de Oração',
    'domestico': 'Culto doméstico',
    'consagracao': 'Consagração',
    'geral': 'Geral'
}

part = 'id,snippet,player,statistics,status'

headers = {'content-type': 'application/json'}

def youtube_request(video_ids):
    formatted_video_ids = str(video_ids)
    payload = {'part': part, 'key': settings.YOUTUBE_KEY, 'id': formatted_video_ids}
    request = requests.get(settings.YOUTUBE_URL, params=payload, headers=headers)
    return request.json()

def create_audit(responsible, changed_model, action_type, obj_name):
    description = 'O administrador {} realizou a ação de {} em "{}" ({}).'.format(responsible, action_type, obj_name, changed_model)
    audit_object = {
        'responsible': responsible,
        'obj_name': obj_name,
        'changed_model': changed_model,
        'action_type': action_type,
        'description': description
    }
    audit = Audit()
    audit.create_audit(audit_object)

def create_push_notification(entity_type, form, entity_id):
    all_devices = NotificationDevice.objects.values_list('device_id', flat=True).distinct()
    all_devices = list(all_devices)

    if len(all_devices) > 0:
        registration_ids = all_devices

        push_service = FCMNotification(api_key=settings.FIREBASE_KEY)

        valid_registration_ids = push_service.clean_registration_ids(registration_ids)

        if len(valid_registration_ids) > 0:
            title = form.cleaned_data['title']
            result = None

            # getting current timezone by OS user timezone
            # local_tz = get_localzone()

            if entity_type == 'video':
                message_title = 'Vídeo novo postado!'
                message_body = 'Um vídeo acabou de ser postado: "' + title + '".'
                data_message = {
                    "entity_type" : entity_type,
                    "entity_id" : entity_id,
                    "redirect" : True
                }
                push_date = timezone.now()
                result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

            elif entity_type == 'event':
                now = timezone.now()
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']

                # locale_start_date = start_date.replace(tzinfo=pytz.utc).astimezone(local_tz)
                # locale_end_date = end_date.replace(tzinfo=pytz.utc).astimezone(local_tz)

                if start_date.day == datetime.now().astimezone(get_localzone()).day and end_date > datetime.now().astimezone(get_localzone()):
                    if start_date > now:
                        message_title = 'Tem evento logo mais!'
                        message_body = 'Se liga nesse evento que vai acontecer hoje: "' + title + '". Fica ligado, pois vai começar às ' + start_date.strftime('%H:%M') + '.'
                    elif start_date <= now and end_date > now:
                        message_title = 'Tem evento acontecendo agora!'
                        message_body = 'Se liga nesse evento que está acontecedo: "' + title + '".'

                    data_message = {
                        "entity_type" : entity_type,
                        "entity_id" : entity_id,
                        "redirect" : True
                    }

                    push_date = now
                    result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

            elif entity_type == 'post':
                now = timezone.now()
                published_date = form.cleaned_data['published_date']
                # if published_date is not None:
                #     locale_published_date = published_date.replace(tzinfo=pytz.utc).astimezone(local_tz)

                if published_date is None or (published_date is not None and published_date <= datetime.now().astimezone(get_localzone())):
                    message_title = 'Postagem nova no app!'
                    if form.cleaned_data['publisher'].nickname is not None:
                        message_body = form.cleaned_data['publisher'].nickname + ' acabou de fazer uma postagem: "' + title + '". Confere lá!'
                    else:
                        message_body = form.cleaned_data['publisher'].name + ' acabou de fazer uma postagem: "' + title + '". Confere lá!'
                    data_message = {
                        "entity_type" : entity_type,
                        "entity_id" : entity_id,
                        "redirect" : True
                    }

                    push_date = now
                    result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

            elif entity_type == 'meeting':
                now = timezone.now()
                start_date = form.cleaned_data['start_date']
                # locale_start_date = start_date.replace(tzinfo=pytz.utc).astimezone(local_tz)

                if start_date.day == datetime.now().astimezone(get_localzone()).day:
                    message_title = 'Hoje tem culto!'

                    if form.cleaned_data['title'] is not None:
                        message_body = 'Fique ligado, pois hoje teremos ' + meeting_types.get(form.cleaned_data['title']) + ' às ' +  start_date.strftime('%H:%M') + '.'
                    else:
                        if form.cleaned_data['organizing_group'] is not None:
                            message_body = 'Fique ligado, pois hoje teremos Programação - ' + form.cleaned_data['organizing_group'].name + ' às ' +  start_date.strftime('%H:%M') + '.'
                        else:
                            message_body = 'Fique ligado, pois hoje teremos Programação Geral às' +  start_date.strftime('%H:%M') + '.'

                    data_message = {
                        "entity_type" : entity_type,
                        "entity_id" : entity_id,
                        "redirect" : True
                    }

                    push_date = now
                    result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

            # Salvando as informações do push notification no banco
            if result is not None:
                save_push_notification_info(message_title, message_body, result, push_date)

        if len(registration_ids) > len(valid_registration_ids):
            delete_invalid_device_ids(valid_registration_ids)

def save_push_notification_info(title, body, result, push_date):
    push_notification_object = {
        'title': title,
        'body': body,
        'multicast_id': result.get('multicast_ids')[0],
        'success_count': result.get('success'),
        'failure_count': result.get('failure'),
        'push_date': push_date
    }
    push_notification = PushNotification()
    push_notification.save_notification(push_notification_object)

def delete_invalid_device_ids(valid_device_ids):
    invalid_device_ids = NotificationDevice.objects.exclude(device_id__in=valid_device_ids)
    invalid_device_ids.delete()

# def schedule_notification_job(push_service, registration_ids, message_title, message_body, data_message, push_date):
#     result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

#     save_push_notification_info(message_title, message_body, result, push_date)

#     return schedule.CancelJob

def get_now_datetime_utc():
    now_date_time = datetime.now()
    # now_date_time.replace(tzinfo=timezone.utc)
    return now_date_time

def get_today_datetime_utc():
    today_date_time = datetime.today()
    # today_date_time.replace(tzinfo=timezone.utc)
    return today_date_time

def get_sunday(sundays_before_index: int):
    today = datetime.today()
    sunday_date = today.strftime('%d/%m/%Y') if today.weekday() == 6 and sundays_before_index == 0 else (today - (timedelta(today.weekday() + 1 + (sundays_before_index * 7)))).strftime('%d/%m/%Y')
    return sunday_date
    