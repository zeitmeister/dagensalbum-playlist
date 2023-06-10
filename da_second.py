from ytmusicapi import YTMusic
import requests
import schedule
import time
import logging
from datetime import date
import json
import os
import base64
import sys
sys.path.append('./models')
from albumgeneratorrequest import AlbumGeneratorRequest
from album import Album
from playlist import Playlist
from searchresults import SearchResults


env = os.getenv('PLAYLIST_ENVIRONMENT_BUILD')
ytmusic = None

logging.basicConfig(filename="./logs/dagensalbum.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

global_playlistId = "temp"

if env == "development":
    logging.info("Running in development mode")
    ytmusic = YTMusic('header-auth.json')

if env == "production":
    logging.info("Running in production mode dawg!")
    header_auth = os.getenv('HEADER_AUTH_JSON')
    json_str = base64.b64decode(header_auth).decode()
    json_dict = json.loads(json_str)
    print(str(json_dict))
    with open('header-auth.json', 'w') as f:
        json.dump(json_dict, f)
    ytmusic = YTMusic('header-auth.json')

try:
    if env == "production":
        global_playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")
    if env == "development":
        global_playlistId = ytmusic.create_playlist("Dagens Album DEV", "En automatiserad playlist av dagens album.")
    f = open('version.json')
    data = json.load(f)
    logging.info("running version: " + data['version'])
    f.close()
except Exception as e:
    logging.error("Error: " + str(e))

playlist = Playlist(logging, ytmusic)
playlist.playlistId = global_playlistId
album = Album()

def run():
    f = open('version.json')
    data = json.load(f)
    logging.info("New day, new album!?")
    logging.info("running version: " + data['version'])
    f.close()
    try:
        agr = AlbumGeneratorRequest(logging)

        if not bool(playlist.playlistId):
            if bool(global_playlistId):
                playlist.playlistId = global_playlistId
            else:
                playlist.create_playlist()
        search_result = SearchResults(logging, ytmusic)
        if (agr.get_json_response()):
            parse_agr = agr.compare_with_yesterday(album)
            if not parse_agr:
                logging.info("The album is the same as yesterday. Stopping execution")
                return False
            else:
                album.set_current_album(agr.agr_artist, agr.agr_title, agr.agr_youtubeMusicId)
        try:
            logging.info('playlistId: ' + playlist.playlistId)
            playlist.set_playlist_json(ytmusic.get_playlist(playlist.playlistId))
        except Exception as e:
            logging.error("Could not set playlist json: " + str(e))
            return False

        if not playlist.clear_playlist():
            logging.info("Could not clear playlist. Trying to delete playlist and create a new one")
            if not playlist.delete_playlist():
                raise ValueError("Could not delete playlist")
            else:
                if not playlist.create_playlist():
                    raise ValueError("Could not create playlist")
        if not search_result.get_album_from_audioplaylistId(album, playlist):
            raise ValueError("Something went wrong when getting album with the help from 1001 albums generator")
            if search_result.search(album.arist, album.title):
                if search_result.parse_search(album, playlist):
                    logging.info("Code executed with no errors today: " + str(date.today()))
        else:
            logging.info("Code executed with no errors today: " + str(date.today()))
    except Exception as e:
        logging.warning("The playlist was not updated for some reason. Reason : " + str(e))


if env == "production":
    # schedule.every().day.at("06:00").do(run)
    schedule.every(60).seconds.do(run)
if env == "development":
    schedule.every(10).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
