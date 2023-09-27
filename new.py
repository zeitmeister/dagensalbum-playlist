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
sys.path.append('./helpers')
from albumgeneratorrequest import AlbumGeneratorRequest
from album import Album
from playlist import Playlist
from searchresults import SearchResults
from program import Program
from helper_functions import HelperFunctions


env = os.getenv('PLAYLIST_ENVIRONMENT_BUILD')
ytmusic = None

logging.basicConfig(filename="./logs/dagensalbum.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

global_playlistId = "temp"
global_yesterdayId = "temp2"
test_id = "temp2"

if env == "development":
    try:
        logging.info("Running in development mode")
        ytmusic = YTMusic('oauth.json')
        print('ytmusic created')
    except Exception as e:
        logging.error("Could not create ytmusic: " + str(e))

if env == "production":
    logging.info("Running in production mode dawg!")
    header_auth = os.getenv('HEADER_AUTH_JSON')
    json_str = base64.b64decode(header_auth).decode()
    json_dict = json.loads(json_str)
    with open('header-auth.json', 'w') as f:
        json.dump(json_dict, f)
    ytmusic = YTMusic('header-auth.json')



try:
    f = open('version.json')

    data = json.load(f)
    logging.info("New day, new album!?")
    logging.info("running supercool version: " + data['version'])
    f.close()
    playlists = ytmusic.get_library_playlists()
    playlistDevId = None
    yesterdaysPlaylistDevId = None
    playlistNames ={
        "todaysProd": 
        {"playlistDescription":"playlistProdId", "playlistName" : "Dagens Album", "playlistId": ""},
        "todaysDev":
        {"playlistDescription":"playlistDevId", "playlistName" : "Dagens Album DEV", "playlistId": ""},
        "yesterdaysProd":
        {"playlistDescription":"yesterdaysPlaylistDevId", "playlistName" : "Gårdagens Album", "playlistId": ""},
        "yesterdaysDev":
        {"playlistDescription":"yesterdaysPlaylistProdId", "playlistName" : "Gårdagens Album DEV", "playlistId": ""}
    }
    playlistNames = HelperFunctions.set_playlist_id(playlistNames, playlists, ytmusic)


    if env == "production":
        if bool(playlistNames["todaysProd"]["playlistId"]):
            global_playlistId = playlistNames["todaysProd"]["playlistId"]
            logging.info('No need to create new playlist')
        else:
            global_playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album my dude.")
            logging.info('Created new playlist for today')

        if bool(playlistNames["yesterdaysProd"]["playlistId"]):
            global_yesterdayId = playlistNames["yesterdaysProd"]["playlistId"]
            logging.info('No need to create new playlist')
        else:
            yesterdaysPlaylistProdId = ytmusic.create_playlist("Gårdagens Album", "En automatiserad playlist av gårdagens album my dude.")
            logging.info('Created new playlist for yesterday')
    if env == "development":
        if bool(playlistNames["todaysDev"]["playlistId"]):
            global_playlistId = playlistNames["todaysDev"]["playlistId"]
            logging.info('No need to create new playlist')
        else:
            global_playlistId = ytmusic.create_playlist("Dagens Album DEV", "En automatiserad playlist av dagens album DEV MODE")

        if bool (playlistNames["yesterdaysDev"]["playlistId"]):
            global_yesterdayId = playlistNames["yesterdaysDev"]["playlistId"]
        else:
            global_yesterdayId = ytmusic.create_playlist("Gårdagens Album DEV", "En automatiserad playlist av gårdagens album DEV MODE")
    f = open('version.json')
    data = json.load(f)
    logging.info("running version: " + data['version'])
    f.close()
except Exception as e:
    logging.error("Error: " + str(e))


yesterdaysPlaylist = Playlist(logging, ytmusic)
yesterdaysPlaylist.playlistId = global_yesterdayId
yesterdaysPlaylist.set_playlist_json(ytmusic.get_playlist(global_yesterdayId))


playlist = Playlist(logging, ytmusic)
playlist.playlistId = global_playlistId
playlist.set_playlist_json(ytmusic.get_playlist(global_playlistId))
album = Album()
agr = AlbumGeneratorRequest(logging)
search_result = SearchResults(logging, ytmusic)
program = Program(logging, playlist, agr, search_result, yesterdaysPlaylist)

def run():
    global ytmusic

    f = open('version.json')

    data = json.load(f)
    logging.info("New day, new album!?")
    logging.info("running supercool version: " + data['version'])
    f.close()

    try:
        if program.run():
            logging.info("Code executed with no errors today: " + str(date.today()))

    except Exception as e:
        logging.warning("The playlist was not updated for some reason. Reason : " + str(e))



if env == "production":
    schedule.every().day.at("06:00").do(run)
if env == "development":
    schedule.every(10).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
