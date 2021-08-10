from typing import Any
import requests
from .auth import Auth


class SpotifyAPI:
    '''
    This class is used to interact with the Spotify Web API.
    '''

    _SPOTIFY_API_VERSION: str = 'v1'
    _SPOTIFY_API_URL: str = f'https://api.spotify.com/{_SPOTIFY_API_VERSION}/'

    def __init__(self, auth: Auth) -> None:
        self._auth: Auth = auth

    def get_artist(self, id_: str) -> dict[str, Any]:
        '''
        Get artist information.

        Args:
            id_ (str): The Spotify ID of the artist.

        Returns:
            dict[str, Any]: The artist information.
        '''

        ...

    def get_new_releases(self) -> dict[str, Any]:
        '''
        Get new releases from the Spotify Web API.

        Returns:
            dict[str, Any]: The new releases.
        '''

        ...

    def get_me(self) -> dict[str, Any]:
        self._raise_for_empty_token()

        headers: dict[str, str] = {
            'Authorization': self._auth.token.bearer,
            'Accept': 'application/json',
        }
        response: requests.Response = requests.get(
            f'{self._SPOTIFY_API_URL}me',
            headers=headers,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise SpotifyAPIError(e)

        return response.json()

    def _raise_for_empty_token(self) -> None:
        if not self._auth.token:
            raise SpotifyAPIError('No token available.')


class SpotifyAPIError(Exception):
    ...
