import os
from pathlib import Path
from gmusicapi import Musicmanager, Mobileclient


_CRED_PATH_MM = str(Path.home().joinpath(".kotone-cred-mm.json"))
_CRED_PATH_MC = str(Path.home().joinpath(".kotone-cred-mc.json"))


def _new_mm() -> Musicmanager:
    if not os.path.exists(_CRED_PATH_MM):
        Musicmanager.perform_oauth(_CRED_PATH_MM)
    mm = Musicmanager()
    if not mm.login(_CRED_PATH_MM):
        raise RuntimeError("login failed")
    return mm


def _new_mc(device_id: str) -> Mobileclient:
    if not os.path.exists(_CRED_PATH_MC):
        Mobileclient.perform_oauth(_CRED_PATH_MC)
    mc = Mobileclient()
    if not mc.oauth_login(device_id, _CRED_PATH_MC):
        raise RuntimeError("login failed")
    return mc

