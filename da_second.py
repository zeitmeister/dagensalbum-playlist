from ytmusicapi import YTMusic
import requests
import schedule
import time
import logging
from datetime import date
import pytest

ytmusic = YTMusic('header-auth.json')

logging.basicConfig(filename="./logs/dagensalbum2-"+str(date.today())+".log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


global_playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")

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
        global global_playlistId
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
                try:
                    ytmusic.delete_playlist(self.playlistId)
                    global_playlistId = None
                    logging.info("Playlist deleted. Creating it again...")
                    self.playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")
                    logging.info("Playlist recreated")
                    return True
                except Exception as e:
                    logging.warning("Could not remove or create the playlist again, no real ways to continue. Crashing...")
                    return False
            return True
        return True


    def delete_playlist(self):
        try:
            ytmusic.delete_playlist(self.playlistId)
            return True
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
    try:
        agr = AlbumGeneratorRequest()
        album = Album()
        if not bool(playlist.playlistId):
            if bool(global_playlistId):
                playlist.playlistId = global_playlistId
            else:
                print("We shoudl not be here")
                playlist.playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")
        search_result = SearchResults()
        if (agr.get_json_response()):
            parse_agr = agr.parse_data(album)
            if not parse_agr:
                raise ValueError("Could not parse data from album generator")
        if not playlist.clear_playlist():
            raise ValueError("Something went wrong when handling the playlist")
        if not search_result.search(album.artist, album.title):
            raise ValueError("Something went wrong when performing search on youtube music")
        if search_result.parse_search(album, playlist):
            logging.info("Code executed with no errors today: " + str(date.today()))
    except Exception as e:
        logging.error("Could not run the program. Error : " + str(e))



schedule.every().day.at("06:00").do(run)
# schedule.every(20).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)

