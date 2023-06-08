from searchresults import SearchResults
class Program:
    def __init__(self, logging, playlist, agr):
        self.logging = logging
        self.playlist = playlist
        self.agr = agr
        self.album = None

    def ensure_playlistId(self, global_playlistId):
        if not bool(self.playlist.playlistId):
            if bool(global_playlistId):
                self.playlist.playlistId = global_playlistId
            else:
                self.playlist.create_playlist()
    
    def compare_with_yesterday(self):
        if (self.agr.get_json_response()):
            parse_agr = self.agr.compare_with_yesterday(album)
            if not parse_agr:
                logging.info("The album is the same as yesterday. Stopping execution")
                return False
            else:
                return True
        else:
            return False

    def set_album(self, agr):
        return self.album.set_current_album(agr.agr_artist, agr.agr_title, agr.agr_youtubeMusicId)

    def clear_or_delete_playlist(self):
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


    def search_and_populate(self):
        search_result = SearchResults(logging, ytmusic)
        if not search_result.get_album_from_audioplaylistid(self.album, self.playlist):
            raise valueerror("something went wrong when getting album with the help from 1001 albums generator")
            if search_result.search(self.album.arist, self.album.title):
                if search_result.parse_search(self.album, self.playlist):
                    logging.info("code executed with no errors today: " + str(date.today()))
        else:
            logging.info("code executed with no errors today: " + str(date.today()))
            return False


    def run(self):
        if not self.ensure_playlistId(self.playlist.playlistId):
            logging.error("Could not ensure the playlistId")
            return False
        if not self.compare_with_yesterday():
            logging.info("Could not compare with yesterday")
        if not self.set_album(self.agr):
            logging.error("Could not set album")
            return False
        if not self.clear_or_delete_playlist():
            logging.error("The playlist is in a failed state. Stopping execution")
            return False
        if not self.search_and_populate():
            logging.error("Could not search and populate")
        logging.info("Code executed with no errors today: " + str(date.today()))
        return True

