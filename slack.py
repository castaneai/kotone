import json
import requests

KOTONE_URL = 'https://kotone-dot-morning-tide.appspot.com'


def notify_slack(webhook_url: str, songs):
    requests.post(webhook_url, data=json.dumps({
        'text': 'New song from Kotone',
        'attachments': [create_attachment(song) for song in songs]
    }))


def create_attachment(song):
    download_url = f"{KOTONE_URL}/api/download/{song['id']}"
    attachment = {
        'title': song['title'],
        'title_link': download_url,
        'text': download_url,
        'author_name': song['artist'],
    }
    if 'albumArtRef' in song:
        attachment['image_url'] = song['albumArtRef'][0]['url']

    return attachment
