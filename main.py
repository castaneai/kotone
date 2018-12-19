import os
import kotone

mc = kotone._new_mc(os.environ["KOTONE_DEVICE_ID"])
mm = kotone._new_mm()

ss = mm.get_purchased_songs()[0]
song =  next(s for s in mc.get_all_songs() if s["id"] == ss["id"])

print(song)

# print(f"downloading... {song['title']}")
# name, data = mm.download_song(song["id"])
# with open(name, "wb") as f:
#   f.write(data)
