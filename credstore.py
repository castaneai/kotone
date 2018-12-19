from gmusicapi.clients import Mobileclient, Musicmanager
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from google.cloud import datastore

_ds = datastore.Client()
_KEY_CRED_MC = _ds.key('KotoneCredentials', 'mc')
_KEY_CRED_MM = _ds.key('KotoneCredentials', 'mm')


def get_flows():
    flow_mc = OAuth2WebServerFlow(**Mobileclient._session_class.oauth._asdict())
    flow_mm = OAuth2WebServerFlow(**Musicmanager._session_class.oauth._asdict())
    return flow_mc, flow_mm


def get_creds():
    cred_mc_entity = _ds.get(_KEY_CRED_MC)
    cred_mm_entity = _ds.get(_KEY_CRED_MM)
    return OAuth2Credentials.from_json(cred_mc_entity['credentials']), OAuth2Credentials.from_json(cred_mm_entity['credentials'])


def save_creds(cred_mc: OAuth2Credentials, cred_mm: OAuth2Credentials):
    cred_mc_entity = datastore.Entity(_KEY_CRED_MC, exclude_from_indexes=('credentials',))
    cred_mc_entity.update({'credentials': cred_mc.to_json()})
    cred_mm_entity = datastore.Entity(_KEY_CRED_MM, exclude_from_indexes=('credentials',))
    cred_mm_entity.update({'credentials': cred_mm.to_json()})
    _ds.put_multi([cred_mc_entity, cred_mm_entity])
