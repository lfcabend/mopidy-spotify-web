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

- ``Mopidy`` >= 0.19.0. The music server that Mopidy-Spotify-Tunigo extends.

- ``Mopidy-Spotify`` >= 1.2.0. The Mopidy extension for playing music from
  Spotify.

- ``Spotipy``. A library for accessing the Spotify web-api.

- ``requests``. HTTP for Humans.

Installation
============

install the package from PyPI::

    pip install Mopidy-Spotify-Web


Configuration
=============

To run this extension you need to authorize it against you Spotify account, to do this visit
https://www.mopidy.com/authenticate/#spotify and follow the instructions.

Example configuration::

    [spotify_web]
    client_id = ... client_id value you got from mopidy.com ...
    client_secret = ... client_secret value you got from mopidy.com ...

The following configuration values are available:

- ``spotify_web/enabled``: If the Spotify extension should be enabled or not.
  Defaults to ``true``.

- ``spotify_web/client_id``: Your Spotify application client id. You *must* provide this.

- ``spotify_web/client_secret``: Your Spotify application secret key. You *must* provide this.

- ``spotify_web/mopidy_token_url``: url to the authorization endpoint
  of the Mopidy OAuth bridge for Spotify. Defaults to https://auth.mopidy.com/spotify/token.

- ``spotify_web/use_mopidy_oauth_bridge``: Use this flag to switch between the Mopidy OAuth bridge and spotify
  authentication service. Defaults to true.

- ``spotify_web/refresh_token``: Your Spotify refresh token. This only needs to be provided if you
  do not want to use the Mopidy OAuth bridge.

- ``spotify_web/spotify_token_url``: url to the authorization endpoint
  of the Spotify Accounts service. Defaults to https://accounts.spotify.com/api/token.


Note:
  In order to use mopidy-spotify-web the plugin requires to authenticate using OAuth. The
  easiest way is to use the OAuth bridge from Mopidy. This is configured as a default.
  If you do not wish to use this service on mopidy.com you can authenticate with Spotify directly.
  In order to do this you need to setup an application on https://developer.spotify.com/my-applications/
  and then follow the tutorial on https://developer.spotify.com/web-api/tutorial/ to obtain a refresh_token.
  The refresh token must then be configured in the Mopidy configuration file. Please make sure to include the
  ``user-library-read`` scope when requesting the refresh token.

Project resources
=================

- `Source code <https://github.com/lfcabend/mopidy-spotify-web>`_
- `Issue tracker <https://github.com/lfcabend/mopidy-spotify-web/issues>`_
- `Download development snapshot
  <https://github.com/lfcabend/mopidy-spotify-web/archive/master.tar.gz#egg=Mopidy-Spotify-Web-dev>`_


Changelog
=========

v0.3.0 (2016-01-24)
-------------------

- Albums are now sorted by track number

v0.2.0 (2015-06-25)
-------------------

- Use ``requests`` module for fetching tokens.
- Blocking initialization moved out of critical startup path.
- Various internal cleanups to make code more Pythonic.
- Switch to using Mopidy's token swap service for simpler authentication.
- Sorted the albums and artists.
- Integrated Spotify browse feature.
- Added feature to browse all albums and top tracks of your artists.

v0.1.0 (2015-05-03)
-------------------

- Initial release.
