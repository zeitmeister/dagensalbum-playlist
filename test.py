from ytmusicapi import YTMusic
import time
import logging
from datetime import date

ytmusic = YTMusic('header-auth.json')

logging.basicConfig(filename="./logs/test-"+str(date.today())+".log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logging.error("Me i expected it to happen")
search_results = ytmusic.search("Sepultura Arise", "albums")
logging.info(search_results)
print(search_results)

