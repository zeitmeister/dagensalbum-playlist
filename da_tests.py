import pytest
import da_second

def pytest_configure():
    album = da_second.Album()

def test_get_album():

    album = da_second.Album()
    assert album.set_current_album("Supertramp", "Crime of the century") == True

def test_no_album_should_throw():
    album = da_second.Album()
    with pytest.raises(Exception):
        album.configurepset_current_album("Supertramp", "")

def test_no_artist_should_throw():
    album = da_second.Album()
    with pytest.raises(Exception):
        album.set_current_album("", "Crime of the century")

def test_no_artist_should_throw():
    album = da_second.Album()
    with pytest.raises(Exception):
        album.set_current_album(None, "Crime of the century")

def test_json_response():
    agr = da_second.AlbumGeneratorRequest()
    album = da_second.Album()
    agr.set_json_response({"currentAlbum" : {"artist" : "Supertramp", "title": "Crime of the century"}})
    agr.parse_data(album)
    assert album.artist == "Supertramp" and album.title == "Crime of the century"

def test_no_currentAlbum_returns_false():
    agr = da_second.AlbumGeneratorRequest()
    album = da_second.Album()
    agr.set_json_response({"artist" : "supertramp", "title": "crime of the century"})
    assert agr.parse_data(album) == False

def test_no_artist_or_title_returns_false():

    agr = da_second.AlbumGeneratorRequest()
    album = da_second.Album()
    agr.set_json_response({"currentAlbum" : {"title": "Crime of the century"}})
    assert agr.parse_data(album) == False

def test_playlist_tracklist_length_zero_is_false():

    playlist = da_second.Playlist()
    playlist.set_tracklist([])
    assert len(playlist.tracklist) == 0

def test_playlist_length():

    playlist = da_second.Playlist()
    playlist.set_tracklist([1,2,3])
    assert len(playlist.tracklist) == 3

