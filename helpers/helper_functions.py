from types import SimpleNamespace
class HelperFunctions:
 #first set the ids of the playlists that actually exists in ytmusic
    def set_playlist_id(playlistDict2, playlistsFromYtmusic, ytmusic):
        for key, value in playlistDict2.items():
            playlistName = playlistDict2[key]["playlistName"]
            for playlist in playlistsFromYtmusic:
                if playlist['title'] == playlistName:
                    playlistDict2[key]["playlistId"] = playlist['playlistId']
                    print("Found playlist id: " + playlistDict2[key]["playlistName"])
                    break
#if some playlist does not exist, create it and set the id
        for key, value in playlistDict2.items():
            if not playlistDict2[key]["playlistId"]:
                try:
                    newId = ytmusic.create_playlist(playlistDict2[key]["playlistName"], "Created by YTMusicPlaylistConverter")
                    playlistDict2[key]["playlistId"] = newId
                except Exception as e:
                    playlistDict2[key]["playlistId"] = None
                    print("Error creating playlist: " + str(e) + ". Setting the id to None")

        return playlistDict2
