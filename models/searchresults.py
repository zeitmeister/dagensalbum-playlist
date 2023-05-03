class SearchResults:

    def __init__(self, logging, ytmusic):
        self.logging = logging
        self.ytmusic = ytmusic

    searchres = dict()

    def search(self, artist, title):
        try:
            self.logging.info("SEARCHRESULT: Todays artist: " + artist)
            self.logging.info("SEARCHRESULT: Todays album title: " + title)
            self.searchres = self.ytmusic.search(title + " " + artist, "albums")
            return True
        except Exception as e:
            self.logging.error("SEARCHRESULT: Could not search youtube music. Error: " + str(e))
            return False


    def parse_search(self, album, playlist):
        if bool(self.searchres):
            if "browseId" in self.searchres[0]:
                browseId = self.searchres[0]["browseId"]
                ytmusicalbum = self.ytmusic.get_album(browseId)
                
                if bool(ytmusicalbum):
                    album.nrOfSongs = len(ytmusicalbum['tracks'])
                    return playlist.populate_playlist(ytmusicalbum, album)
            else:
                self.logging.info("SEARCHRESULT: No browseId from search result")
                return False

        else:
            self.logging.info("SEARCHRESULT: No search result... Trying to get the album from Alexander's api instead")
            return False

    def get_album_from_audioplaylistId(self, album, playlist):
        try:
            browseId = self.ytmusic.get_album_browse_id(album.audioPlaylistId)
            ytmusicalbum = self.ytmusic.get_album(browseId)
            if bool(ytmusicalbum):
                album.nrOfSongs = len(ytmusicalbum['tracks'])
                self.logging.info("SEARCHRESULT: Got album from audioPlaylistId")
                return playlist.populate_playlist(ytmusicalbum, album)
            else:
                self.logging.info("SEARCHRESULT: No album from audioPlaylistId")
                return False
        except Exception as e:
            self.logging.error("SEARCHRESULT: Could not get album from audioPlaylistId. Error: " + str(e))
            return False


