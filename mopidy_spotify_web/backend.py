from __future__ import unicode_literals

import logging

from mopidy import backend

import pykka

from mopidy_spotify_web.library import SpotifyWebLibraryProvider

logger = logging.getLogger(__name__)


class SpotifyWebBackend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(SpotifyWebBackend, self).__init__()
        logger.debug("initializing mopidy-web backend")
        self.config = config

        self.library = SpotifyWebLibraryProvider(backend=self)

        self.uri_schemes = ['spotifyweb']
