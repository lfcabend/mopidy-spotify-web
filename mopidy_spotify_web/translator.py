from __future__ import unicode_literals

from mopidy.models import Track
from mopidy.models import Artist
from mopidy.models import Album


def to_mopidy_tracks(spotipy_items):
    tracks = []
    for item in spotipy_items:
        tracks.append(to_mopidy_track(item['track']))
    return tracks


def to_mopidy_track(track):
    return Track(uri=track['uri'],
                     name=track['name'],
                     album=to_mopidy_album(track['album']),
                     artists=to_mopidy_artists(track['artists']))


def to_mopidy_artists(spotipy_artists):
    artists = []
    for artist in spotipy_artists:
        uri = "spotifyweb:artist:%s" % artist['id']
        artists.append(Artist(name=artist['name'], uri=uri))
    return artists


def to_mopidy_album(spotipy_album):
    uri = "spotifyweb:album:%s" % spotipy_album['id']
    return Album(name=spotipy_album['name'], uri=uri)