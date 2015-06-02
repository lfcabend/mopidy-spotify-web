from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import Ref

import requests

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
        auth = (config['spotify_client_id'], config['spotify_client_secret'])
        response = requests.post(config['auth_server_url'], auth=auth, data={
            'grant_type': 'refresh_token',
            'refresh_token': config['refresh_token'],
        })
        logger.debug("authentication response: %s", response.content)
        access_token = response.json()['access_token']
        logger.debug("authentication token: %s", access_token)
        return access_token
    except requests.exceptions.RequestException as e:
        logger.error('Refreshing the auth token failed: %s', e)
    except ValueError as e:
        logger.error('Decoding the JSON auth token response failed: %s', e)


class SpotifyWebLibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri='spotifyweb:directory',
                                   name='Spotify Web Browse')

    def __init__(self, *args, **kwargs):
        super(SpotifyWebLibraryProvider, self).__init__(*args, **kwargs)
        self._cache = None
        self._root = [
            Ref.directory(uri='spotifyweb:artists', name='Artists'),
            Ref.directory(uri='spotifyweb:albums', name='Albums')]

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
        self.sortedAlbums = []
        self.sortedArtists = []
        self.tracks = []
        for t in tracks:
            logger.debug("Adding track %s", t.name)
            self.tracks.append(Ref.track(name=t.name, uri=t.uri))
            if hasattr(t, 'album'):
                self.add_album_and_artists(t)

        logger.debug('Sorting albums and artists')
        cmp_dir_names = lambda x, y: cmp(x.name, y.name)
        self.sortedAlbums.sort(cmp_dir_names)
        self.sortedArtists.sort(cmp_dir_names)

    def add_album_and_artists(self, track):
        album = track.album

        name = album.name
        logger.debug('Going to add album %s', name)
        album_dir = Ref.directory(uri=album.uri, name=name)
        track_ref = Ref.track(name=track.name, uri=track.uri)
        if album.uri not in self.albums2tracks:
            self.sortedAlbums.append(album_dir)

        # adding track to album2tracks
        if album.uri in self.albums2tracks:
            if track_ref not in self.albums2tracks[album.uri]:
                self.albums2tracks[album.uri].append(track_ref)
        else:
            self.albums2tracks[album.uri] = [track_ref]

        if hasattr(track, 'artists'):
            self.add_artists(track, album_dir)

    def add_artists(self, track, album_dir):
        for artist in track.artists:
            artist_name = artist.name
            logger.debug('Going to add artist %s', artist_name)

            artist_dir = Ref.directory(uri=artist.uri, name=artist_name)
            if artist.uri not in self.artists2albums:
                self.sortedArtists.append(artist_dir)

            if artist.uri in self.artists2albums:
                if album_dir not in self.artists2albums[artist.uri]:
                    self.artists2albums[artist.uri].append(album_dir)
            else:
                self.artists2albums[artist.uri] = [album_dir]
