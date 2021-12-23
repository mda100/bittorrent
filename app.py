# (for pirate bay i will need magents and DHT; i also want a UI)

from bencodepy import decode, encode
from hashlib import sha1
from random import randint 
from requests import get

FILE_PATH = '/Users/martinadams/Desktop/bittorrent/debian-mac-11.2.0-amd64-netinst.iso.torrent'

class TorrentFile:
    def __init__(self, filename) -> None:
        self.filename = filename
        with open(self.filename, 'rb') as f:
            self.meta_info = f.read()
            self.torrent = decode(self.meta_info)
        pass

class Torrent:
    def __init__(self, torrent_file) -> None:
        self.announce = torrent_file[b'announce'].decode("utf-8")
        self.comment = torrent_file[b'comment']
        self.creation_date = torrent_file[b'creation date']
        self.httpseeds = torrent_file[b'httpseeds']
        self.info = torrent_file[b'info']
        pass
    
class Tracker:
    def __init__(self, torrent) -> None:
        self.announce_url = torrent.announce
        self.info_hash = sha1(encode(torrent.info))
        self.peer_id =  '-PC0001-' + ''.join([str(randint(0, 9)) for _ in range(12)])
        self.uploaded = 0
        self.downloaded = 0
        self.left =  torrent.info[b'length'] - self.downloaded
        self.port = 6889
        self.compact = 1
        pass

    def connect(self):
            response = get(
                f"{self.announce_url}?info_hash={self.info_hash}&peer_id={tracker.peer_id}&uploaded={self.uploaded}&downloaded={self.downloaded}&left={self.left}&port={self.port}&compact={self.compact}",
                headers={
                    "Content-Length": "363",
                    "Content-Type": "text/plain",
                    "Pragma": "no-cache",
                    "User-Agent": "Chrome/70.0.3538.77"
                    }
                )
            if not response.status == 200:
                raise ConnectionError('Unable to connect to traacker')
            else: 
                return response

torrent_file = TorrentFile(FILE_PATH)
torrent = Torrent(torrent_file.torrent)
tracker = Tracker(torrent)
tracker.connect()

## ok i got this far, having trouble connecting to the client
## so step one is get this connection successful and get a response
## step two is create a method / class for connecting to a singular peer
## and updating the tracker accordingly
## and have a class for the full data 
## then have an event loop that does all this asynchronously and returns the data at the end