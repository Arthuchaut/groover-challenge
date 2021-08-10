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

    def get_artist(id_: str) -> dict[str, Any]:
        ...

    def get_new_releases() -> dict[str, Any]:
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
