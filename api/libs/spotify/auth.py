import os
import base64
from typing import Union
from django.utils.encoding import filepath_to_uri


class Credentials:
    '''
    The credentials class.

    Attributes:
        client_id (str): The client id.
        _client_secret (str): The client secret.
    '''

    def __init__(self, client_id: str, client_secret: str) -> None:
        '''
        The constructor.

        Args:
            client_id (str): The client id.
            client_secret (str): The client secret.
        '''

        self.client_id: str = client_id
        self._client_secret: str = client_secret

    @property
    def _b64_creds(self) -> str:
        '''
        Returns the base64 encoded credentials.

        Returns:
            str: The base64 encoded credentials.
        '''

        return base64.b64encode(
            f'{self.client_id}:{self._client_secret}'.encode()
        ).decode('utf-8')

    @property
    def bearer(self) -> str:
        '''
        Returns the bearer token.

        Returns:
            str: The bearer token.
        '''

        return f'Bearer {self._b64_creds}'


class Auth:
    '''
    The Spotify Auth class.
    The authentication process is using OAuth2 protocol.

    Attributes:
        _AUTHORIZE_URL (str): The Spotify authorize url.
        _TOKEN_URL (str): The Spotify token url.
        _creds (Credentials): The credentials.
        _scope (list[str]): The scope.
        _redirect_uri (str): The redirect uri.
    '''

    _AUTHORIZE_URL: str = 'https://accounts.spotify.com/authorize/'
    _TOKEN_URL: str = 'https://accounts.spotify.com/api/token/'

    def __init__(
        self, creds: Credentials, scope: list[str], redirect_uri: str
    ) -> None:
        '''
        The constructor.

        Args:
            creds (Credentials): The credentials.
            scope (list[str]): The scope.
            redirect_uri (str): The redirect uri.
        '''

        self._creds: Credentials = creds
        self._scope: list[str] = scope
        self._redirect_uri: str = redirect_uri

    def _url_encode(self, obj: Union[list[str], str]) -> str:
        '''
        Encodes the object in URL format.

        Args:
            obj (Union[list[str], str]): The object to encode.

        Returns:
            str: The URL encoded object.
        '''

        if isinstance(obj, list):
            return '%20'.join(obj)
        else:
            return filepath_to_uri(obj)

    @property
    def authorize_url(self) -> str:
        '''
        Returns the Spotify authorize url.

        Returns:
            str: The authorize url.
        '''

        params: dict[str, str] = {
            'response_type': 'code',
            'client_id': self._creds.client_id,
            'scope': self._url_encode(self._scope),
            'redirect_uri': self._url_encode(self._redirect_uri),
        }

        return (
            self._AUTHORIZE_URL
            + '?'
            + '&'.join(f'{k}={v}' for k, v in params.items())
        )
