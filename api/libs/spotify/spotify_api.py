from typing import Any, Iterator
import time
import requests
from .auth import Auth


class SpotifyAPI:
    '''
    This class is used to interact with the Spotify Web API.
    '''

    _SPOTIFY_API_VERSION: str = 'v1'
    _SPOTIFY_API_URL: str = f'https://api.spotify.com/{_SPOTIFY_API_VERSION}/'
    PAGE_SIZE: int = 20

    def __init__(self, auth: Auth) -> None:
        self._auth: Auth = auth

    def _get(
        self, resource: str, params: dict[str, Any] = {}
    ) -> dict[str, Any]:
        '''
        Get information from the Spotify Web API.

        Args:
            resource (str): The Spotify Web API URL.
            params (dict[str, Any]): The query parameters.
                Default to {}.

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

        while True:
            response: requests.Response = requests.get(
                self._SPOTIFY_API_URL + resource,
                headers=headers,
                params=params,
            )

            try:
                response.raise_for_status()
                break
            except requests.HTTPError as e:
                # Figure out the 429 error which is usually due to the
                # requests rate limit.
                # We wait for a few seconds (given by the "Retry-After"
                # header) and try again.
                # We had +1 second to ensure that the waiting time is filled.
                if response.status_code == 429:
                    time.sleep(int(response.headers['Retry-After']) + 1)
                else:
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

    def get_several_artists(self, ids: list[str]) -> dict[str, Any]:
        '''
        Get several artists information.

        Args:
            ids (list[str]): The Spotify IDs of the artists.
                The maximum number of IDs is 50.

        Raises:
            SpotifyAPIError: If the maximum number of IDs is exceeded 50
                or if the request fails.

        Returns:
            dict[str, Any]: The artists information.
        '''

        if len(ids) > 50:
            raise SpotifyAPIError(
                f'The maximum number of artists IDs '
                f'must be lower or equal to 50. '
                f'{len(ids)} IDs given.'
            )

        params: dict[str, str] = {
            'ids': ','.join(ids),
        }
        response: dict[str, Any] = self._get(resource='artists', params=params)

        return response['artists']

    def get_new_releases(self) -> Iterator[dict[str, Any]]:
        '''
        Get new releases from the Spotify Web API.

        Raises:
            SpotifyAPIError: If the request fails.

        Returns:
            Iterator[dict[str, Any]]: The new releases generator.
        '''

        resource: str = 'browse/new-releases'
        params: dict[str, Any] = {
            'offset': 0,
            'limit': self.PAGE_SIZE,
        }

        while True:
            response: dict[str, Any] = self._get(resource, params)
            response = response['albums']
            total: int = response['total']
            offset: int = response['offset']
            limit: int = response['limit']
            params['offset'] = offset + limit

            for item in response.get('items'):
                yield item

            if offset + limit >= total:
                break

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
