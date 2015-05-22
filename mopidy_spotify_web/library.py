from __future__ import unicode_literals

import base64
import json
import logging
import urllib
import urllib2

from mopidy import backend
from mopidy.models import Ref

import spotipy

from translator import to_mopidy_track

logger = logging.getLogger(__name__)


def get_tracks_from_web_api(token):
    try:
        logger.debug('Loading spotify-web library from '
                     'web-api using token: %s', token)
        sp = spotipy.Spotify(auth=token)
        con = True
        offset = 0
        limit = 50
        tracks = []
        while con:
            results = sp.current_user_saved_tracks(
                limit=limit, offset=offset)
            size = len(results['items'])
            logger.debug('On spotify-web Got results %s for '
                         'offset %s', str(size), str(offset))
            if size > 0:
                for item in results['items']:
                    tracks.append(to_mopidy_track(item['track']))
                offset += size

            if results['next'] is None:
                con = False
        return tracks
    except spotipy.SpotifyException as e:
        logger.error('Spotipy error({0}): {1}'.format(e.code, e.msg))
        return []


def get_fresh_token(config):
    try:
        logger.debug("authenticating")
        auth_server_token_refresh_url = \
            config['spotify_web']['auth_server_url']
        client_id = config['spotify_web']['spotify_client_id']
        client_secret = config['spotify_web']['spotify_client_secret']
        auth_buffer = '%s:%s' % (client_id, client_secret)
        buffer_base_64 = base64.b64encode(auth_buffer)
        authorization_header = 'Basic %s' % buffer_base_64
        refresh_token = config['spotify_web']['refresh_token']
        payload = urllib.urlencode({'grant_type': 'refresh_token',
                                    'refresh_token': refresh_token})
        request = urllib2.Request(auth_server_token_refresh_url, data=payload)
        request.add_header('Authorization', authorization_header)
        content = urllib2.urlopen(request).read()
        logger.debug("authentication response: %s", content)
        json_body = json.loads(content)
        access_token = json_body['access_token']
        logger.debug("authentication token: %s", access_token)
        return access_token
    except urllib2.URLError as e:
        logger.error('While posting auth config, '
                     'URLError error: {0}, {1}'.format(e.reason, e.message))
    except urllib2.HTTPError as e:
        logger.error('While posting auth config, '
                     'HTTPError error({0}): {1}'.format(e.errno, e.strerror))


class SpotifyWebLibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri='spotifyweb:directory',
                                   name='Spotify Web Browse')

    def __init__(self, *args, **kwargs):
        super(SpotifyWebLibraryProvider, self).__init__(*args, **kwargs)
        logger.debug("initializing SpotifyWebLibraryProvider "
                     "from mopidy-web backend")
        self._root = [Ref.directory(uri='spotifyweb:artists',
                                    name='Artists'),
                      Ref.directory(uri='spotifyweb:albums',
                                    name='Albums')]
        self._cache = None
        self.refresh()

    def refresh(self, uri=None):
        token = get_fresh_token(self.backend.config)
        if token is not None:
            tracks = get_tracks_from_web_api(token)
        else:
            tracks = []

        self._cache = Cache(tracks)

    def lookup(self, uri):
        pass

    def browse(self, uri):
        logger.debug("Request to browse %s in SpotifyWebLibraryProvider", uri)
        if uri == self.root_directory.uri:
            return self._root
        elif uri == 'spotifyweb:artists':
            return self._cache.sortedArtists
            # return Ref directory with all artists
        elif uri.startswith('spotifyweb:artist:'):
            # get artist uri
            return self._cache.artists2albums.get(uri)
            # return Ref directory with all albums for artist
        elif uri.startswith('spotifyweb:album:'):
            # get album uri
            return self._cache.albums2tracks.get(uri)
            # return Ref directory with all tracks for album
        elif uri == 'spotifyweb:albums':
            return self._cache.sortedAlbums
            # return Ref directory for all albums
        else:
            return []


class Cache:
    def __init__(self, tracks, *args, **kwargs):
        logger.debug("initializing SpotifyWebLibraryProvider cache")
        self.albums2tracks = {}
        self.artists2albums = {}
        self.sortedAlbums = set()
        self.sortedArtists = set()
        self.tracks = set()
        for t in tracks:
            logger.debug("Adding track %s", t.name)
            self.tracks.add(Ref.track(name=t.name, uri=t.uri))
            if hasattr(t, 'album'):
                self.add_album_and_artists(t)

    def add_album_and_artists(self, track):
        album = track.album

        name = album.name
        logger.debug('Going to add album %s', name)
        album_dir = Ref.directory(uri=album.uri, name=name)
        track_ref = Ref.track(name=track.name, uri=track.uri)
        self.sortedAlbums.add(album_dir)

        # adding track to album2tracks
        if album.uri in self.albums2tracks:
            self.albums2tracks[album.uri].add(track_ref)
        else:
            self.albums2tracks[album.uri] = set([track_ref])

        if hasattr(track, 'artists'):
            self.add_artists(track, album_dir)

    def add_artists(self, track, album_dir):
        for artist in track.artists:
            artist_name = artist.name
            logger.debug('Going to add artist %s', artist_name)

            artist_dir = Ref.directory(uri=artist.uri, name=artist_name)
            self.sortedArtists.add(artist_dir)

            if artist.uri in self.artists2albums:
                self.artists2albums[artist.uri].add(album_dir)
            else:
                self.artists2albums[artist.uri] = set([album_dir])
