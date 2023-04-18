from ytmusicapi import YTMusic
import requests
import schedule
import time
import logging
from datetime import date
import json
import os
import base64

ytmusic = None

logging.basicConfig(filename="./logs/dagensalbum2-"+str(date.today())+".log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

if env == "development":
    logging.info("Running in development mode")
    ytmusic = YTMusic('header-auth.json')
if env == "production":
    logging.info("Running in production mode")
    header_auth = os.getenv('HEADER_AUTH_JSON')
    json_str = base64.b64decode(header_auth).decode()
    json_dict = json.loads(json_str)
    with open('header-auth.json', 'w') as f:
        json.dump(json_dict, f)
    ytmusic = YTMusic('header_auth_json')

global_playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")
global_artist = None
global_title = None

f = open('version.json')
data = json.load(f)
logging.info("running version: " + data['version'])
f.close()
class SearchResults:

    searchres = dict()

    def search(self, artist, title):
        try:
            logging.info("Todays artist: " + artist)
            logging.info("Todays album title: " + title)
            self.searchres = ytmusic.search(title + " " + artist, "albums")
            return True
        except Exception as e:
            logging.error("Could not search youtube music. Error: " + str(e))
            return False


    def parse_search(self, album, playlist):
        if bool(self.searchres):
            if "browseId" in self.searchres[0]:
                browseId = self.searchres[0]["browseId"]
                ytmusicalbum = ytmusic.get_album(browseId)
                
                if bool(ytmusicalbum):
                    album.nrOfSongs = len(ytmusicalbum['tracks'])
                    return playlist.populate_playlist(ytmusicalbum, album)
            else:
                logging.info("No browseId from search result")
                return False

        else:
            logging.info("No search result... Guess there'll be no playlist today")
            return False

class Album:

    artist = None
    title = None
    nrOfSongs = None

    def set_current_album(self, artist, title):
        if not artist or not title:
            raise Exception
        self.artist = artist
        self.title = title
        return True

class Playlist:

    tracklist = []
    playlistId = None

    def set_tracklist(self, tl):
        self.tracklist = tl

    def clear_playlist(self):
        if not bool(self.update_tracklist()):
            return False
        if bool(self.tracklist) and len(self.tracklist) > 0:
            logging.info("Track list is not empty. Starting to remove tracks...")
            try:
                ytmusic.remove_playlist_items(self.playlistId, self.tracklist)
                self.tracklist.clear()
                logging.info("Playlist cleared")
                return True
            except Exception as e:
                logging.warning("Could not empty playlist. Error is :" + str(e))
                return False
        return True

    def update_tracklist(self):
        try:
            playlist = ytmusic.get_playlist(self.playlistId)
            if playlist['trackCount'] != len(self.tracklist):
                logging.info("Tracklist is not up to date. Updating...")
                self.tracklist.clear()
                for track in playlist['tracks']:
                    trackDict = {
                        "videoId" : track['videoId'],
                        "setVideoId" : track['setVideoId']
                    }
                    self.tracklist.append(trackDict)
                logging.info("Tracklist updated")
                return True
            else:
                return True
        except Exception as e:
            logging.warning("Could not update tracklist. Error is :" + str(e))
            return False


    def delete_playlist(self):
        try:
            ytmusic.delete_playlist(self.playlistId)
            return True
            logging.info("Playlist deleted")
        except Exception as e:
            logging.warning("Could not delete playlist. Error is :" + str(e))
            return False

    def create_playlist(self):
        try:
            playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist för dagens album")
            self.playlistId = playlistId
            return True

        except Exception as e:
            logging.warning("Could not create playlist. Error is :" + str(e))
            return False

    def populate_playlist(self, ytmusicalbum, class_album):
        if 'tracks' in ytmusicalbum:
            for track in ytmusicalbum['tracks']:
                trackId = track['videoId']
                try:
                    result = ytmusic.add_playlist_items(self.playlistId, [trackId])
                    logging.info("Track: " + track["title"] + " added to playlist.")
                    trackDict = {
                        "videoId" : trackId,
                        "setVideoId" : result['playlistEditResults'][0]['setVideoId']
                    }
                    self.tracklist.append(trackDict)
                except Exception as e:
                    logging.info("Could not add track to playlist. Error: " + str(e))
                time.sleep(2)
            self.track_count = ytmusic.get_playlist(self.playlistId)["trackCount"]
        else:
            logging.info("No tracks in album from youtube music")
            return False

        if ytmusic.get_playlist(self.playlistId)["trackCount"] == class_album.nrOfSongs:
            logging.info("Album completely added to playlist")
            return True
        else:
            logging.warning("Album not completely added to playlist. Some tracks appear to be missing")
            return False


class AlbumGeneratorRequest:

    response = dict()

    def set_json_response(self, res):
        self.response = res

    def get_json_response(self):
        try:
            url = "https://1001albumsgenerator.com/api/v1/projects/simon"
            response = requests.get(url)
            response_json = response.json()
            self.set_json_response(response_json)
            return True
        except Exception as e:
            logging.error("Could not make request to album generator. No internet? Error is: " + str(e))
            return False

    def compare_with_yesterday(self, global_album):
        global global_artist, global_title
        if global_album.artist == global_artist and global_album.title == global_title:
            logging.info("Album is the same as yesterday. No need to update playlist")
            return False
        else:
            logging.info("Album is different from yesterday. Updating playlist")
            global_album.set_current_album(self.response['currentAlbum']['artist'], self.response['currentAlbum']['name'])
            global_artist = global_album.artist
            global_title = global_album.title
            return True
        return False
        logging.warning("No current album")
        return False

    def parse_data(self, global_album):
        if 'currentAlbum' in self.response:

            if 'artist' in self.response['currentAlbum'] and 'name' in self.response['currentAlbum']:
                global_album.set_current_album(self.response['currentAlbum']['artist'], self.response['currentAlbum']['name'])
                return True
            else:
                print("No artist or title")
                return False
        else:
            print("No current album")
            return False


playlist = Playlist()
playlist.playlistId = global_playlistId

def run():
    f = open('version.json')
    data = json.load(f)
    logging.info("running version: " + data['version'])
    f.close()
    try:
        agr = AlbumGeneratorRequest()
        album = Album()
        if not bool(playlist.playlistId):
            if bool(global_playlistId):
                playlist.playlistId = global_playlistId
            else:
                playlist.playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")
        search_result = SearchResults()
        if (agr.get_json_response()):
            parse_agr = agr.parse_data(album)
            if not parse_agr:
                raise ValueError("Could not parse data from album generator")
            if not agr.compare_with_yesterday(album):
                raise ValueError("Album is the same as yesterday. No need to update playlist")
        if not playlist.clear_playlist():
            logging.info("Could not clear playlist. Trying to delete playlist and create a new one")
            if not playlist.delete_playlist():
                raise ValueError("Could not delete playlist")
            else:
                if not playlist.create_playlist():
                    raise ValueError("Could not create playlist")
        if not search_result.search(album.artist, album.title):
            raise ValueError("Something went wrong when performing search on youtube music")
        if search_result.parse_search(album, playlist):
            logging.info("Code executed with no errors today: " + str(date.today()))
    except Exception as e:
        logging.error("Could not run the program. Error : " + str(e))



schedule.every().day.at("06:00").do(run)
# schedule.every(40).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)

