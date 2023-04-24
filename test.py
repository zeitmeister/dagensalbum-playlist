from ytmusicapi import YTMusic
import time
import logging
from datetime import date
import os

ytmusic = YTMusic('header-auth.json')

logging.basicConfig(filename="./logs/test-"+str(date.today())+".log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logging.error("Me i expected it to happen")

album = ytmusic.get_album_browse_id("OLAK5uy_kc5UNFZYKSe85ERJt10h59QRSJoJth4rc")
print(album)
# for track in album['tracks']:
#         logging.info("Track: " + track["title"] + " added to playlist.")
secret = os.environ.get('DAGENS_SECRET')
print(secret)
