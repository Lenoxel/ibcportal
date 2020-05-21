import requests
from django.conf import settings
from datetime import datetime
from django.utils import timezone
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
    'oracao': 'Ciclo de Oração',
    'domestico': 'Culto doméstico'
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
        push_service = FCMNotification(api_key=settings.FIREBASE_KEY)

        if entity_type == 'video':
            title = form.cleaned_data['title']

        registration_ids = all_devices

        message_title = 'Vídeo novo postado!'
        message_body = 'Um vídeo acabou de ser postado: "' + title + '"' 
        data_message = {
            "entity_type" : entity_type,
            "entity_id" : entity_id,
            "redirect" : True
        }

        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

        save_push_notification_info(message_title, message_body, result)
        # Salvando as informações do push notification

def save_push_notification_info(title, body, result):
    push_notification_object = {
        'title': title,
        'body': body,
        'multicast_id': result.get('multicast_ids')[0],
        'success_count': result.get('success'),
        'failure_count': result.get('failure'),
        'push_date': datetime.now(timezone.utc)
    }
    push_notification = PushNotification()
    push_notification.save_notification(push_notification_object)

    
    
            