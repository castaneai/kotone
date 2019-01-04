import oauth2client.client
from typing import Tuple
from gmusicapi import Musicmanager, Mobileclient

_UPLOADER_ID = '60:98:75:FD:D5:0F'
_UPLOADER_NAME = 'Kotone'


class Kotone:

    def __init__(self, device_id: str, cred_mc: oauth2client.client.OAuth2Credentials, cred_mm: oauth2client.client.OAuth2Credentials):
        self._mc = Mobileclient()
        if not self._mc.oauth_login(device_id, cred_mc):
            raise RuntimeError('Mobileclient login failed')
        self._mm = Musicmanager()
        if not self._mm.login(cred_mm, _UPLOADER_ID, _UPLOADER_NAME):
            raise RuntimeError('Musicmanager login failed')

    def get_songs(self):
        return self._mc.get_all_songs()

    def download_song(self, song_id: str) -> Tuple[str, bytes]:
        return self._mm.download_song(song_id)
