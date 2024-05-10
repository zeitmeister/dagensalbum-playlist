from ytmusicapi import YTMusic
import time
import logging
from datetime import date
import os
import sys
# sys.path.append('models')
# print(sys.path)
from models.playlist import Playlist
import json

# Open and load JSON file
ytmusic = YTMusic('oauth.json')

logging.basicConfig(filename="./logs/dagensalbum.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logging.error("Me i expected it to happen")
#
# album = ytmusic.get_album_browse_id("OLAK5uy_lKfyal6hd8SK6_OW_pYS9eQscYjemiVWI")
# logging.info(album)
#
# # ytmusicalbum = ytmusic.get_album(album)
# # if bool(ytmusicalbum):
# #     # print(ytmusicalbum)
# #     # nrOfSongs = len(ytmusicalbum['tracks'])
# #     # print(nrOfSongs)
# # else:
# #     self.logging.info("No album from audioPlaylistId")
temp = ytmusic.get_album_browse_id('PLDIxWXRU4UDpUpAB4vMTUroYuvodq118L')
# ytmusicalbum = ytmusic.get_album(temp)
# print(ytmusicalbum)
temp2 = ytmusic.get_album_browse_id('OLAK5uy_kVH9MhQbG4JKBBFConZXzvYEDT_ATuIhI')
album = ytmusic.get_album(temp2)
# print(album)
print(temp)
# print(temp2)

if (bool(temp)):
    print("Album found")

# playlists = ytmusic.get_library_playlists()
# for playlistYT in playlists:
#
#     if playlistYT['title'] == "Dagens Album":
#         print(playlistYT['title'])
#         print(playlistYT['playlistId'])
#         print("Playlist found")
#         playlistId = playlistYT['playlistId']
#         classPlaylist = Playlist(logging, ytmusic)
#         classPlaylist.playlistId = playlistId
#         playlistObj = ytmusic.get_playlist(playlistId)
#         classPlaylist.set_playlist_json(playlistObj)
#         removed = classPlaylist.clear_playlist()
#         if removed:
#             print("Playlist cleared")
#         else:
#             print("Failed to clear playlist")
#
#         # nrOfSongs = len(playlist['tracks'])
#         print(len(playlistObj['tracks']))
#         break
# for track in album['tracks']:
#         logging.info("Track: " + track["title"] + " added to playlist.")
# secret = os.environ.get('DAGENS_SECRET')
# print(secret)
