import os
from pathlib import Path
from gmusicapi import Musicmanager, Mobileclient

cred_path = str(Path.home().joinpath(".kotone-cred.json"))
if not os.path.exists(cred_path):
    Mobileclient.perform_oauth(cred_path)
    print(f"save credentials to {cred_path}")

mc = Mobileclient()
device_id = os.environ["KOTONE_DEVICE_ID"]
if not mc.oauth_login(device_id, cred_path):
    raise RuntimeError('login failed')

for song in mc.get_all_songs():
    print(song["title"])
