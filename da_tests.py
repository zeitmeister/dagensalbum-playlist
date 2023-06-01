import pytest
import pytest_mock
import sys
sys.path.append('./models')
from album import Album
from albumgeneratorrequest import AlbumGeneratorRequest
from playlist import Playlist
from program import Program

def pytest_configure():
    album = da_second.Album()

def test_get_album(global_album):
    assert global_album.set_current_album("Supertramp", "Crime of the century", "hej") == True

def test_no_album_should_throw(global_album):
    with pytest.raises(Exception): global_album.set_current_album("Supertramp", "")

def test_no_artist_should_throw(global_album):
    with pytest.raises(Exception):
        global_album.set_current_album("", "Crime of the century")

def test_no_artist_should_throw(global_album):
    with pytest.raises(Exception):
        global_album.set_current_album(None, "Crime of the century")

def test_json_response(global_album, global_logging):
    agr = AlbumGeneratorRequest(global_logging)
    agr.set_json_response({"currentAlbum" : {"artist" : "Supertramp", "name": "Crime of the century", "youtubeMusicId" : "korv"}})
    global_album.set_current_album(agr.agr_artist, agr.agr_title, agr.agr_youtubeMusicId)
    assert global_album.artist == "Supertramp" and global_album.title == "Crime of the century"

def test_no_currentAlbum_returns_false(global_album, global_logging):
    agr = AlbumGeneratorRequest(global_logging)
    res = agr.set_json_response({"artist" : "supertramp", "name": "crime of the century", "youtubeMusicId" : "korv"})
    assert res == False

def test_no_artist_or_title_returns_false(global_album, global_logging):
    agr = AlbumGeneratorRequest(global_logging)
    res = agr.set_json_response({"currentAlbum" : {"title": "Crime of the century"}})
    assert res == False

def test_album_is_same_as_yesterday_returns_false(global_album, global_logging):
    agr = AlbumGeneratorRequest(global_logging)
    global_album.set_current_album("Supertramp", "Crime of the century", "hej")
    agr.set_json_response({"currentAlbum" : {"artist" : "Supertramp", "name": "Crime of the century", "youtubeMusicId" : "korv"}})
    res = agr.compare_with_yesterday(global_album)
    assert res == False

def test_album_is_different_from_yesterday_returns_true(global_album, global_logging):
    agr = AlbumGeneratorRequest(global_logging)
    agr.set_json_response({"currentAlbum" : {"artist" : "Supertramp", "name": "Breakfast in America", "youtubeMusicId" : "korv"}})
    global_album.set_current_album("Supertramp", "Crime of the century", "hej")
    res = agr.compare_with_yesterday(global_album)
    assert res == True

def test_album_is_different_from_yesterday_sets_new_album(global_album, global_logging):
    global_album.set_current_album("Supertramp", "Crime of the century", "hej")
    agr = AlbumGeneratorRequest(global_logging)
    agr.set_json_response({"currentAlbum" : {"artist" : "Supertramp", "name": "Breakfast in America", "youtubeMusicId" : "korv"}})
    agr.compare_with_yesterday(global_album)
    assert global_album.artist == "Supertramp" and global_album.title == "Breakfast in America"

def test_playlist_tracklist_length_zero_is_false(global_logging, global_ytmusic):
    playlist = Playlist(global_logging, global_ytmusic)
    playlist.set_tracklist([])
    assert len(playlist.tracklist) == 0

def test_playlist_length(global_logging, global_ytmusic):
    playlist = Playlist(global_logging, global_ytmusic)
    playlist.set_tracklist([1,2,3])
    assert len(playlist.tracklist) == 3

def test_update_playlist(global_logging, global_ytmusic):
    playlist = Playlist(global_logging, global_ytmusic)
    playlist.set_tracklist([1,2,3])
    playlist.set_playlist_json({
  "trackCount": 11,
  "tracks": [
    { "videoId": "abc123", "setVideoId": "def456" },
    { "videoId": "ghi789", "setVideoId": "jkl012" },
    { "videoId": "mno345", "setVideoId": "pqr678" },
    { "videoId": "stu901", "setVideoId": "vwx234" },
    { "videoId": "yzab56", "setVideoId": "cde789" },
    { "videoId": "fgh012", "setVideoId": "ijk345" },
    { "videoId": "lmn678", "setVideoId": "opq901" },
    { "videoId": "rst234", "setVideoId": "uvw567" },
    { "videoId": "xyz890", "setVideoId": "abc123" },
    { "videoId": "def456", "setVideoId": "ghi789" },
    { "videoId": "jkl012", "setVideoId": "mno345" }
  ]
})  
    playlist.update_tracklist()
    assert len(playlist.tracklist) == len(playlist.playlist_json["tracks"])

def test_update_playlist_same_length(global_logging, global_ytmusic):
    playlist = Playlist(global_logging, global_ytmusic)
    playlist.set_tracklist([1,2,3])
    playlist.set_playlist_json({
  "trackCount": 3,
  "tracks": [
    { "videoId": "abc123", "setVideoId": "def456" },
    { "videoId": "ghi789", "setVideoId": "jkl012" },
    { "videoId": "mno345", "setVideoId": "pqr678" }
  ]
})  
    playlist.update_tracklist()
    assert len(playlist.tracklist) == playlist.playlist_json["trackCount"]

def test_program_playlistId(global_logging, global_ytmusic, global_album, global_playlist):
    agr = AlbumGeneratorRequest(global_logging)
    program = Program(global_logging, global_playlist, agr)
    program.playlist.playlistId = "hej"
    assert program.playlist.playlistId != None

def test_create_playlist_is_called_if_no_playlistId(global_logging, global_ytmusic, global_album, global_playlist, mocker):
    global_playlistId = ""

    agr = AlbumGeneratorRequest(global_logging)
    program = Program(global_logging, global_playlist, agr)
    mock_create_playlist = mocker.spy(program.playlist, 'create_playlist')
    program.playlist.playlistId = None
    program.ensure_playlistId(global_playlistId)
    assert mock_create_playlist.call_count == 1

def test_program_returns_false_if_could_not_get_json_from_agr(global_logging, global_ytmusic, mocker):
    mocker.patch('albumgeneratorrequest.AlbumGeneratorRequest.get_json_response', return_value = False)
    agr = AlbumGeneratorRequest(global_logging)
    program = Program(global_logging, global_ytmusic, agr)
    assert program.compare_with_yesterday() == False

def test_program_calls_delete_if_clear_playlist_is_false(global_logging, global_playlist, global_ytmusic, mocker):

    agr = AlbumGeneratorRequest(global_logging)
    program = Program(global_logging, global_playlist, agr)
    mocker.patch.object(program.playlist, 'clear_playlist', return_value = False)
    spy = mocker.spy(program.playlist, 'delete_playlist')
    program.clear_or_delete_playlist()
    assert spy.call_count == 1

def test_program_creates_playlist_if_delete_playlist_is_true(global_logging, global_playlist, global_ytmusic, mocker):
    agr = AlbumGeneratorRequest(global_logging)
    program = Program(global_logging, global_playlist, agr)
    mocker.patch.object(program.playlist, 'clear_playlist', return_value = False)
    mocker.patch.object(program.playlist, 'delete_playlist', return_value = True)
    spy = mocker.spy(program.playlist, 'create_playlist')
    program.clear_or_delete_playlist()
    assert spy.call_count == 1

def test_program_clearordelete_is_false_if_delete_is_true_and_create_is_false(global_logging, global_playlist, global_ytmusic, mocker):
    agr = AlbumGeneratorRequest(global_logging)
    program = Program(global_logging, global_playlist, agr)
    mocker.patch.object(program.playlist, 'clear_playlist', return_value = False)
    spy = mocker.patch.object(program.playlist, 'delete_playlist', return_value = True)
    mocker.patch.object(program.playlist, 'create_playlist', return_value = False)
    result = program.clear_or_delete_playlist()
    assert result == False

def test_program_clearordelete_is_false_if_delete_is_true_and_create_is_true(global_logging, global_playlist, global_ytmusic, mocker):
    agr = AlbumGeneratorRequest(global_logging)
    program = Program(global_logging, global_playlist, agr)
    mocker.patch.object(program.playlist, 'clear_playlist', return_value = False)
    spy = mocker.patch.object(program.playlist, 'delete_playlist', return_value = True)
    mocker.patch.object(program.playlist, 'create_playlist', return_value = True)
    result = program.clear_or_delete_playlist()
    assert result == True
