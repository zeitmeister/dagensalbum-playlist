class Album:

    artist = None
    title = None
    nrOfSongs = None
    audioPlaylistId = None

    def set_current_album(self, artist, title, audioId):
        if not artist or not title:
            return False
        self.artist = artist
        self.title = title
        self.audioPlaylistId = audioId
        return True

