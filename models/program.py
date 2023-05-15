class Program:
    def __init__(self, logging, playlist):
        self.logging = logging
        self.playlist = playlist
        self.album = None
    
    def ensure_playlist_exists(self):
        if bool(self.playlist.playlistId):
            print("Playlist exists")

        # if bool(global_playlistId):
        #     playlist.playlistId = global_playlistId
        else:
            self.playlist.create_playlist()

