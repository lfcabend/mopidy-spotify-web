from __future__ import unicode_literals

from mopidy import backend

import pykka

from mopidy_spotify_web.library import SpotifyWebLibraryProvider


class SpotifyWebBackend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(SpotifyWebBackend, self).__init__()
        self.config = config['spotify_web']
        self.library = SpotifyWebLibraryProvider(backend=self)
        self.uri_schemes = ['spotifyweb']
