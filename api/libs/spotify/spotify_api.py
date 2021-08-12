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

    def _get(
        self, resource: str, params: dict[str, Any] = None
    ) -> dict[str, Any]:
        '''
        Get information from the Spotify Web API.

        Args:
            url (str): The Spotify Web API URL.

        Raises:
            SpotifyAPIError: If the request fails.

        Returns:
            dict[str, Any]: The response.
        '''

        self._raise_for_empty_token()
        headers: dict[str, str] = {
            'Authorization': self._auth.token.bearer,
            'Accept': 'application/json',
        }
        response: requests.Response = requests.get(
            self._SPOTIFY_API_URL + resource, headers=headers, params=params
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise SpotifyAPIError(e)

        return response.json()

    def get_artist(self, id_: str) -> dict[str, Any]:
        '''
        Get artist information.

        Args:
            id_ (str): The Spotify ID of the artist.

        Returns:
            dict[str, Any]: The artist information.
        '''

        return self._get(resource=f'artists/{id_}')

    def get_new_releases(self) -> dict[str, Any]:
        '''
        Get new releases from the Spotify Web API.

        Raises:
            SpotifyAPIError: If the request fails.

        Returns:
            dict[str, Any]: The new releases.
        '''

        return self._get(resource='browse/new-releases')

    def get_me(self) -> dict[str, Any]:
        '''
        Get the current user's information.

        Raises:
            SpotifyAPIError: If the request fails.

        Returns:
            dict[str, Any]: The user's information.
        '''

        return self._get(resource='me')

    def _raise_for_empty_token(self) -> None:
        '''
        Raises an error if the token is empty.

        Raises:
            SpotifyAPIError: If the token is empty.
        '''

        if not self._auth.token:
            raise SpotifyAPIError('No token available.')


class SpotifyAPIError(Exception):
    ...
