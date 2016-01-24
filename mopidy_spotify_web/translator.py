from __future__ import unicode_literals

from mopidy.models import Album, Artist, Track


def to_mopidy_tracks(spotipy_items):
    tracks = []
    for item in spotipy_items:
        tracks.append(to_mopidy_track(item['track']))
    return tracks


def to_mopidy_track(track):
    return Track(uri=track['uri'],
                 name=track['name'],
                 album=to_mopidy_album(track['album']),
                 artists=to_mopidy_artists(track['artists']),
                 track_no=track['track_number'])


def to_mopidy_artists(spotipy_artists):
    artists = []
    for artist in spotipy_artists:
        uri = 'spotifyweb:yourmusic:artist:%s' % artist['id']
        artists.append(Artist(name=artist['name'], uri=uri))
    return artists


def to_mopidy_album(spotipy_album):
    uri = 'spotifyweb:yourmusic:album:%s' % spotipy_album['id']
    return Album(name=spotipy_album['name'], uri=uri)


def to_sauce_uri(uri):
    ids = uri.split(':')
    artist_id = ids[3]
    return 'spotifyweb:sauce:artist:%s' % artist_id
