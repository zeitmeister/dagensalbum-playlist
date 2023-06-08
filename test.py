from ytmusicapi import YTMusic
import time
import logging
from datetime import date
import os

ytmusic = YTMusic('header-auth.json')

logging.basicConfig(filename="./logs/dagensalbum.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logging.error("Me i expected it to happen")

album = ytmusic.get_album_browse_id("OLAK5uy_lKfyal6hd8SK6_OW_pYS9eQscYjemiVWI")
logging.info(album)

ytmusicalbum = ytmusic.get_album(album)
if bool(ytmusicalbum):
    print(ytmusicalbum)
    nrOfSongs = len(ytmusicalbum['tracks'])
else:
    self.logging.info("No album from audioPlaylistId")
# for track in album['tracks']:
#         logging.info("Track: " + track["title"] + " added to playlist.")
secret = os.environ.get('DAGENS_SECRET')
print(secret)
