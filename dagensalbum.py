from ytmusicapi import YTMusic
import requests
import schedule
import time
import logging
from datetime import date
import pytest

#authenticate ytmusic

ytmusic = YTMusic('header-auth.json')

logging.basicConfig(filename="./logs/dagensalbum-"+str(date.today())+".log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

# create a playlist when the app starts
playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")
todays_title = None
todays_artist = None
album = None
nrOfSongs = None

# create an empty track list
track_list = []




def find_album(title, artist):

    global playlistId, album, nrOfSongs

    if len(track_list) > 0:
        logging.info("Track list is not empty. Starting removing them...")
        try:
            ytmusic.remove_playlist_items(playlistId, track_list)
            track_list.clear()
            logging.info("Playlist cleared")
        except Exception as e:
            logging.warning("Could not remove tracks from the playlist. Error: " + str(e) + ". Removin playlist instead")
            try:
                ytmusic.delete_playlist(playlistId)
                logging.info("Playlist deleted. Creating it again...")
                playlistId = ytmusic.create_playlist("Dagens Album", "En automatiserad playlist av dagens album.")
                logging.info("Playlist created")
            except Exception as e:
                logging.warning("Could not remove or create the playlist again, no real ways to continue. Crashing...")
                raise e
    
    # perform a search on ytmusic with the provided artist and title

    search_results = ytmusic.search(title + " " + artist, "albums")
    if bool(search_results):
        if "browseId" in search_results[0]:
            browseId = search_results[0]['browseId']
            album = ytmusic.get_album(browseId)
            if bool(album):
                nrOfSongs = len(album['tracks'])
                populate_playlist(album)
            else:
                logging.info("Could not find any album from the search result. This is an unelikely error. Perhaps something is wrong with your/my code")
        else:
            logging.info("No browseId found. Perhaps the resulttype was not an album?")
    else:
        logging.info("No album found... Guess there'll be no playlist today")




def populate_playlist(album):

    global playlistId, track_list, nrOfSongs
    playlistTrackCount = ytmusic.get_playlist(playlistId)["trackCount"]
    while playlistTrackCount != nrOfSongs:
        # loop through the tracks from the album and add it to the playlist
        for track in album['tracks']:
            trackId = track['videoId']
            try:
                result = ytmusic.add_playlist_items(playlistId, [trackId])
                logging.info("Track: " + track["title"] + " added to playlist. ")

                # create a dict with videoId and setVideoId that's needed when tracks are removed from the playlist
                trackDict = {
                    "videoId" : trackId,
                    "setVideoId" : result['playlistEditResults'][0]['setVideoId']
                }
                track_list.append(trackDict)
            except Exception as e:
                logging.warning("Could not add track to the playlist. Error is: " + str(e))
                time.sleep(2)
                try:
                    logging.info("Trying to add the track again")
                    result = ytmusic.add_playlist_items(playlistId, [trackId])
                    logging.info("Track: " + track["title"] + " added to playlist. ")

                    # create a dict with videoId and setVideoId that's needed when tracks are removed from the playlist
                    trackDict = {
                        "videoId" : trackId,
                        "setVideoId" : result['playlistEditResults'][0]['setVideoId']
                    }
                    # append the dict to the list of dicts
                    track_list.append(trackDict)
                except Exception as e:
                    logging.warning("Second attempt to add track was not successful either, skipping this track. Error is: " + str(e))
            time.sleep(1)
            playlistTrackCount = ytmusic.get_playlist(playlistId)["trackCount"]
    logging.info("Album completely added to playlist")



def stuff():
    try:
        album1 = Album()
        global todays_artist, todays_title

        logging.info('Running version 0.2.0')

        # get current album

        # try:
        url = "https://1001albumsgenerator.com/api/v1/projects/simon"
        response = requests.get(url)
        response_json = response.json()

        # set artist and album title

        artist = response_json['currentAlbum']['artist']
        title = response_json['currentAlbum']['name']
        logging.info(artist)
        logging.info(title)
        print(artist)
        print(title)

        if title != todays_title and artist != todays_artist:
            todays_artist = artist
            todays_title = title
            find_album(todays_title, todays_artist)
        else:
            logging.info("Album appears to be the same as yesterday, perhaps it's saturday or sunday?")
        # except Exception as e:


    except Exception as e:
        logging.error("Could not get todays album. Perhaps there's no internet connection... Error is: " + str(e))


def stuff2():

    logging.info("halloj")


# schedule.every().day.at("06:00").do(stuff)
schedule.every(60).seconds.do(stuff)



# while True:
#     schedule.run_pending()
#     time.sleep(1)
