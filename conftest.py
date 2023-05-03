import pytest
import sys
import logging
from datetime import date
sys.path.append('./models')
from album import Album

logging.basicConfig(filename="./logs/dagensalbum2-"+str(date.today())+".log",
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
