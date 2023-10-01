import time

class Playlist:

    def __init__(self, logging, ytmusic):
        self.logging = logging
        self.ytmusic = ytmusic

    tracklist = []
    playlistId = None
    playlist_json = None

    def set_tracklist(self, tl):
        self.tracklist = tl

    def set_playlist_json(self, playlist_json):
        self.playlist_json = playlist_json

    def clear_playlist(self):
        if not bool(self.update_tracklist()):
            return False
        if bool(self.tracklist) and len(self.tracklist) > 0:
            self.logging.info("PLAYLIST: Track list is not empty. Starting to remove tracks...")
            try:
                self.ytmusic.remove_playlist_items(self.playlistId, self.tracklist)
                self.tracklist.clear()
                self.logging.info("PLAYLIST: Playlist cleared")
                return True
            except Exception as e:
                self.logging.warning("PLAYLIST: Could not empty playlist. Error is :" + str(e))
                return False
        return True



    def update_tracklist(self):
        try:
            if self.playlist_json['trackCount'] != len(self.tracklist):
                self.logging.info(str(self.playlist_json['trackCount']) + " the playlist has  tracks")
                self.logging.info("Tracklist is not up to date. Updating...")
                self.tracklist.clear()
                for track in self.playlist_json['tracks']:
                    trackDict = {
                        "videoId" : track['videoId'],
                        "setVideoId" : track['setVideoId']
                    }
                    self.tracklist.append(trackDict)
                self.logging.info("PLAYLIST: Tracklist updated")
                return True
            else:
                self.logging.info('Tracklist up to date. No need to update.')
                return True
        except Exception as e:
            self.logging.warning("PLAYLIST: Could not update tracklist. Error is :" + str(e))
            return False


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
                        trackDict = {
                            "videoId" : trackId,
                            "setVideoId" : result['playlistEditResults'][0]['setVideoId']
                        }
                        self.tracklist.append(trackDict)
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


