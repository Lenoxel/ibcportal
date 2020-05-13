import requests
from django.conf import settings

part = 'id,snippet,player,statistics,status'

headers = {'content-type': 'application/json'}

def youtube_request(video_ids):
    formatted_video_ids = str(video_ids)
    payload = {'part': part, 'key': settings.YOUTUBE_KEY, 'id': formatted_video_ids}
    request = requests.get(settings.YOUTUBE_URL, params=payload, headers=headers)
    return request.json()