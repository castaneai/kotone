from typing import Tuple, Optional
from gmusicapi.clients import Mobileclient, Musicmanager
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from google.cloud import datastore
from pathlib import Path


class CredStoreBase:

    def get_creds(self) -> Tuple[Optional[OAuth2Credentials], Optional[OAuth2Credentials]]:
        raise NotImplementedError()

    def save_creds(self, cred_mm: OAuth2Credentials, cred_mc: OAuth2Credentials):
        raise NotImplementedError()


class CloudDatastoreCredStore(CredStoreBase):

    def __init__(self):
        self._ds = datastore.Client()
        self._KEY_CRED_MC = self._ds.key('KotoneCredentials', 'mc')
        self._KEY_CRED_MM = self._ds.key('KotoneCredentials', 'mm')

    def get_creds(self) -> Tuple[Optional[OAuth2Credentials], Optional[OAuth2Credentials]]:
        cred_mc_entity = self._ds.get(self._KEY_CRED_MC)
        cred_mm_entity = self._ds.get(self._KEY_CRED_MM)
        if None in (cred_mc_entity, cred_mm_entity):
            return None, None
        return OAuth2Credentials.from_json(cred_mc_entity['credentials']),\
               OAuth2Credentials.from_json(cred_mm_entity['credentials'])

    def save_creds(self, cred_mc: OAuth2Credentials, cred_mm: OAuth2Credentials):
        cred_mc_entity = datastore.Entity(self._KEY_CRED_MC, exclude_from_indexes=('credentials',))
        cred_mc_entity.update({'credentials': cred_mc.to_json()})
        cred_mm_entity = datastore.Entity(self._KEY_CRED_MM, exclude_from_indexes=('credentials',))
        cred_mm_entity.update({'credentials': cred_mm.to_json()})
        self._ds.put_multi([cred_mc_entity, cred_mm_entity])


class LocalCredStore(CredStoreBase):

    def __init__(self):
        self._PATH_CRED_MC = Path.home().joinpath('.kotone-cred-mc.json')
        self._PATH_CRED_MM = Path.home().joinpath('.kotone-cred-mm.json')

    def get_creds(self) -> Tuple[Optional[OAuth2Credentials], Optional[OAuth2Credentials]]:
        if not self._PATH_CRED_MC.exists() or not self._PATH_CRED_MM.exists():
            return None, None
        return OAuth2Credentials.from_json(self._PATH_CRED_MC.read_text()),\
               OAuth2Credentials.from_json(self._PATH_CRED_MM.read_text())

    def save_creds(self, cred_mc: OAuth2Credentials, cred_mm: OAuth2Credentials):
        with self._PATH_CRED_MC.open('w') as fmc:
            fmc.write(cred_mc.to_json())
        with self._PATH_CRED_MM.open('w') as fmm:
            fmm.write(cred_mm.to_json())


def get_flows() -> Tuple[OAuth2WebServerFlow, OAuth2WebServerFlow]:
    flow_mc = OAuth2WebServerFlow(**Mobileclient._session_class.oauth._asdict())
    flow_mm = OAuth2WebServerFlow(**Musicmanager._session_class.oauth._asdict())
    return flow_mc, flow_mm
