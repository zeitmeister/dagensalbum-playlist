import pytest
import sys
import logging
from datetime import date
sys.path.append('../models')
from album import Album
from playlist import Playlist

logging.basicConfig(filename="../logs/dagensalbum2-"+str(date.today())+".log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

@pytest.fixture(scope="session")
def global_album():
    album = Album()
    return album

@pytest.fixture(scope="session")
def global_logging():
    return logging

@pytest.fixture(scope="session")
def global_ytmusic():
    ytmusic = None
    return ytmusic

@pytest.fixture(scope="session")
def global_playlist():
    ytmusic = None
    logging2 = logging
    playlist = Playlist(logging2, ytmusic)
    return playlist

@pytest.fixture(scope="session")
def global_yesterdayPlaylist():
    ytmusic = None
    logging2 = logging
    yesterdayPlaylist = Playlist(logging2, ytmusic)
    return yesterdayPlaylist
