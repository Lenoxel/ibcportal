import requests
from django.conf import settings
from .models import Audit


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
            