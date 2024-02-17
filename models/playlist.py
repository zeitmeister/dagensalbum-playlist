import time

class Playlist:

    def __init__(self, logging, ytmusic):
        self.logging = logging
        self.ytmusic = ytmusic

    playlistId = None
    playlist_json = None


    def set_playlist_json(self, playlist_json):
        self.playlist_json = playlist_json

    def set_playlistJsonFromYtMusic(self):
        try:
            self.playlist_json = self.ytmusic.get_playlist(self.playlistId)
            self.logging.info("PLAYLIST: Playlist json set from ytmusic")
            return True
        except Exception as e:
            self.logging.warning("PLAYLIST: Could not set playlist json from ytmusic. Error is :" + str(e))
            return False



    def clear_playlist(self):
        trackDictArr = self.get_trackDictArr()
        if not bool(trackDictArr):
            return False
        if bool(trackDictArr) and len(trackDictArr) > 0:
            self.logging.info("PLAYLIST: Track list is not empty. Starting to remove tracks...")
            try:
                self.ytmusic.remove_playlist_items(self.playlistId, trackDictArr)
                self.logging.info("PLAYLIST: Playlist cleared")
                return True
            except Exception as e:
                self.logging.warning("PLAYLIST: Could not empty playlist. Error is :" + str(e))
                return False
        return True



    def get_trackDictArr(self):
        returnTracklist = []
        try:
            if len(self.playlist_json['tracks']) > 0:
                self.logging.info(str(self.playlist_json['trackCount']) + " the playlist has  tracks")
                for track in self.playlist_json['tracks']:
                    trackDict = {
                        "videoId" : track['videoId'],
                        "setVideoId" : track['setVideoId']
                    }
                    returnTracklist.append(trackDict)
                return returnTracklist
            else:
                self.logging.info('PLAYLIST: Playlist json does not contain any tracks')
                return returnTracklist
        except Exception as e:
            self.logging.warning("PLAYLIST: Could not get trackDictArr. Error is :" + str(e))
            return returnTracklist


    def delete_playlist(self):
        try:
            self.ytmusic.delete_playlist(self.playlistId)
            return True
            self.logging.info("PLAYLIST: Playlist deleted")
        except Exception as e:
            self.logging.warning("PLAYLIST: Could not delete playlist. Error is :" + str(e))
            return False

    def create_playlist(self):
        try:
            playlistId = self.ytmusic.create_playlist("Dagens Album", "En automatiserad playlist för dagens album")
            self.playlistId = playlistId
            return True

        except Exception as e:
            self.logging.warning("PLAYLIST: Could not create playlist. Error is :" + str(e))
            return False

    def add_to_playlist(self, videoIdArray):
        try:
            self.ytmusic.add_playlist_items(self.playlistId, videoIdArray)
            return True
        except Exception as e:
            self.logging.warning("PLAYLIST: Could not add to playlist. Error is :" + str(e))
            return False

    def populate_playlist(self, ytmusicalbum, class_album):
        if 'tracks' in ytmusicalbum:
            for track in ytmusicalbum['tracks']:
                trackId = track['videoId']
                if trackId is None or trackId == "":
                    self.logging.error("PLAYLIST: Could not find video id for track: " + track["title"] +'. Track not added to playlist')
                else:
                    try:
                        result = self.ytmusic.add_playlist_items(self.playlistId, [trackId])
                        self.logging.info("PLAYLIST: Track: " + track["title"] + " added to playlist.")
                    except Exception as e:
                        self.logging.info("PLAYLIST: Could not add track to playlist. Error: " + str(e))
                time.sleep(2)
            self.track_count = self.ytmusic.get_playlist(self.playlistId)["trackCount"]
        else:
            self.logging.info("PLAYLIST: No tracks in album from youtube music")
            return False
        playlist_length = self.ytmusic.get_playlist(self.playlistId)["trackCount"]
        if self.ytmusic.get_playlist(self.playlistId)["trackCount"] == class_album.nrOfSongs:
            self.logging.info("PLAYLIST: Album completely added to playlist")
            return True
        else:
            self.logging.warning("PLAYLIST: Album not completely added to playlist. Only " + str(playlist_length) + " out of " + str(class_album.nrOfSongs) + " added.")
            
            return False


