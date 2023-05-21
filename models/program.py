class Program:
    def __init__(self, logging, playlist, agr):
        self.logging = logging
        self.playlist = playlist
        self.agr = agr
        self.album = None
    
    def ensure_playlist_exists(self):
        if bool(self.playlist.playlistId):
            print("Playlist exists")

        # if bool(global_playlistId):
        #     playlist.playlistId = global_playlistId
        else:
            self.playlist.create_playlist()
    def run(self):
        if (self.agr.get_json_response()):
            parse_agr = self.agr.compare_with_yesterday(album)
            if not parse_agr:
                logging.info("The album is the same as yesterday. Stopping execution")
                return False
            else:
                self.album.set_current_album(agr.agr_artist, agr.agr_title, agr.agr_youtubeMusicId)
        else:
            return False
