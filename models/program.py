from searchresults import SearchResults
from datetime import date
from status import Status
from album import Album
class Program:
    def __init__(self, logging, playlist, agr, search_result, yesterday_playlist):
        self.logging = logging
        self.yesterdaysPlaylist = yesterday_playlist
        self.search_result = search_result
        self.playlist = playlist
        self.agr = agr
        self.album = Album()
        self.status = Status()

    def ensure_playlistId(self, global_playlistId):
        print("global_playlistId: " + global_playlistId)
        if not bool(self.playlist.playlistId):
            if bool(global_playlistId):
                self.playlist.playlistId = global_playlistId
            else:
                self.playlist.create_playlist()
    
    def compare_with_yesterday(self):
        if (self.agr.get_json_response()):
            parse_agr = self.agr.compare_with_yesterday(self.album)
            if not parse_agr:
                return False
            else:
                return True
        else:
            self.status.error = True
            self.status.status_message = "Could not get album from album generator"
            return False

    def set_album(self, agr):
        return self.album.set_current_album(agr.agr_artist, agr.agr_title, agr.agr_youtubeMusicId)

    def clear_or_delete_playlist(self):
        trackDictArr = self.playlist.get_trackDictArr()
        if len(trackDictArr) == 0:
            self.logging.info("Playlist is empty. No need to clear it")
            return True
        if not self.playlist.clear_playlist():
            self.logging.info("Could not clear playlist")
            if self.playlist.delete_playlist():
                if not self.playlist.create_playlist():
                    self.logging.info("Could not create playlist")
                    return False
                else:
                    return True
            else:
                return False
        else:
            return True
    def set_yesterdays_playlist(self):
        try:
            trackDictArr = self.playlist.get_trackDictArr()
            if not bool(trackDictArr):
                self.logging.warning("PROGRAM: Could not get trackDictArr")
                return False
            videoIdArray = []
            if len(trackDictArr) > 0:
                self.logging.info("PROGRAM: The trackDictArr for the current playlist is not empty. Updating yesterdays playlist")
                for track in trackDictArr:
                    videoIdArray.append(track['videoId'])
                self.yesterdaysPlaylist.add_to_playlist(videoIdArray)
                self.logging.info("PROGRAM: Yesterdays playlist updated")
            else:
                self.logging.info("The trackDictArr for the current playlist is empty. So can't update yesterdays playlist")
            return True
        except Exception as e:
            self.logging.warning("PROGRAM: Could not set yesterdays playlist. Error is :" + str(e))
            return False


    def search_and_populate(self):
        if not self.search_result.get_album_from_audioplaylistId(self.album, self.playlist):
            self.logging.warning("Could not get album from audioPlaylistId")
            self.status.error = True
            if self.search_result.search(self.album.artist, self.album.title):
                if self.search_result.parse_search(self.album, self.playlist):
                    self.logging.info("code executed with no errors today1: " + str(date.today()))
                    self.status.error = False
                    self.status.status_message = "No errors"
                    return True
            else:
                self.logging.error("Could not search youtube music")
                self.status.error = True
                self.status.status_message = "Could not search youtube music"
                return False
        else:
            self.logging.info("code executed with no errors today2: " + str(date.today()))
            return True


    def run(self):
        if not self.playlist.playlistId:
            self.logging.error("Could not ensure the playlistId")
            return False
        if not self.playlist.set_playlistJsonFromYtMusic():
            self.logging.error("Could not set playlistJsonFromYtMusic")
            return False
        if not self.set_yesterdays_playlist():
            self.logging.error("Could not set yesterdays playlist")
        if not self.compare_with_yesterday():
            if self.status.status_message == "Could not get album from album generator":
                self.logging.error(self.status.error_message)
                return False
            else:
                self.logging.info("Album is the same as yesterday. No need to update playlist. Stopping execution")
                return True
        if not self.set_album(self.agr):
            self.logging.error("Could not set album")
            return False

        if not self.clear_or_delete_playlist():
            self.logging.error("The playlist is in a failed state. Creating new one...")
            if not self.playlist.create_playlist():
                self.logging.error("Could not create playlist")
                return False
            self.logging.info("New playlist created")
            return True
        if not self.search_and_populate():
            self.logging.error("Could not search and populate")
            return False

        return True

