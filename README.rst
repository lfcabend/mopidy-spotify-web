*********************
Mopidy-Spotify-Web
*********************


`Mopidy <http://www.mopidy.com/>`_ extension for providing the browse feature
of `Spotify <http://www.spotify.com/>`_. This lets you browse artists and albums
of your spotify user account library.

Uses the `Spotipy <https://github.com/plamere/spotipy/>`_ API, which is a python wrapper arround
the spoitify web api.


Dependencies
============

- A Spotify Premium subscription. Mopidy-Spotify will not work with
  Spotify Free, just Spotify Premium.

- A non-Facebook Spotify username and password.

- A registered application on https://developer.spotify.com, follow the instruction
  on https://developer.spotify.com/web-api/tutorial/. Create a  Client ID and Secret Key,
  then finish the tutorial to obtain a refresh token.

- ``Mopidy`` >= 0.19.0. The music server that Mopidy-Spotify-Tunigo extends.

- ``Mopidy-Spotify`` >= 1.2.0. The Mopidy extension for playing music from
  Spotify.

- ``Spotipy``. A library for accessing the Spotify web-api.


Installation
============

install the package from PyPI::

    pip install Mopidy-Spotify-Web


Configuration
=============

Example configuration::

    [spotify_web]
    spotify_client_id = 'YOUR_CLIENT_ID'
    spotify_client_secret = 'YOUR_SECRET'
    refresh_token = 'YOUR_REFRESH_TOKEN'

The following configuration values are available:

- ``spotify/enabled``: If the Spotify extension should be enabled or not.
  Defaults to ``true``.

- ``spotify_web/client_id``: Your Spotify application client id. You *must* provide this.

- ``spotify_web/spotify_client_secret``: Your Spotify application secret key. You *must* provide this.

- ``spotify_web/refresh_token``: Your Spotify refresh token. You *must* provide this.

- ``spotify_web/auth_server_url``: url to the authorization endpoint
  of the Accounts service. You *must* provide this. Should contain https://accounts.spotify.com/api/token


Project resources
=================

- `Source code <https://github.com/lfcabend/mopidy-spotify-web>`_
- `Issue tracker <https://github.com/lfcabend/mopidy-spotify-web/issues>`_
- `Download development snapshot <https://github.com/lfcabend/mopidy-spotify-web/archive/master.tar.gz#egg=Mopidy-Spotify-Web-dev>`_


Changelog
=========

v0.1.0 (2015-05-03)
-------------------

- Initial release.
