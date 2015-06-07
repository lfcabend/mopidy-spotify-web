from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


logger = logging.getLogger(__name__)
logger.debug("loading mopidy-web extension")

__version__ = '0.1.1'


class Extension(ext.Extension):

    dist_name = 'Mopidy-Spotify-Web'
    ext_name = 'spotify_web'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['client_id'] = config.String()
        schema['client_secret'] = config.String()
        schema['mopidy_token_url'] = config.String()
        schema['spotify_token_url'] = config.String()
        schema['use_mopidy_oauth_bridge'] = config.Boolean()
        schema['refresh_token'] = config.String()
        return schema

    def setup(self, registry):
        logger.debug("registering mopidy-web backend")
        from .backend import SpotifyWebBackend
        registry.add('backend', SpotifyWebBackend)
