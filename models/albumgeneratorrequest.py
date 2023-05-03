import requests

class AlbumGeneratorRequest:

    def __init__(self, logging):
        self.logging = logging
    response = dict()

    def set_json_response(self, res):
        self.response = res

    def get_json_response(self):
        try:
            url = "https://1001albumsgenerator.com/api/v1/projects/simon"
            response = requests.get(url)
            response_json = response.json()
            if 'artist' in response_json['currentAlbum'] and 'name' in response_json['currentAlbum'] and 'youtubeMusicId' in response_json['currentAlbum']:
                self.set_json_response(response_json)
                return True
            else:
                self.logging.warning("AGR: All keys not present in response")
                return False
        except Exception as e:
            self.logging.error("Could not make request to album generator. No internet? Error is: " + str(e))
            return False

    def compare_with_yesterday(self, global_album):
        if global_album.artist == self.response['currentAlbum']['artist'] and global_album.title == self.response['currentAlbum']['name']:
            self.logging.info("AGR: Album is the same as yesterday. No need to update playlist")
            return False
        else:
            self.logging.info("AGR: Album is different from yesterday. Updating playlist")
            global_album.set_current_album(self.response['currentAlbum']['artist'], self.response['currentAlbum']['name'], self.response['currentAlbum']['youtubeMusicId'])
            return True
        return False
        self.logging.warning("AGR: No current album")
        return False



