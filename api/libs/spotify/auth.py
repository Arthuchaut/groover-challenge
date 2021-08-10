import base64
import requests
from typing import Union
from django.utils.encoding import filepath_to_uri
from user.models import User


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
    def _b64creds(self) -> str:
        '''
        Returns the base64 encoded credentials.

        Returns:
            str: The base64 encoded credentials.
        '''

        return base64.b64encode(
            f'{self.client_id}:{self._client_secret}'.encode()
        ).decode('utf-8')

    @property
    def basic(self) -> str:
        '''
        Returns the basic authentication string.

        Returns:
            str: The basic authentication string.
        '''

        return f'Basic {self._b64creds}'


class Token:
    '''
    The token class.

    Attributes:
        access_token (str): The access token.
        token_type (str): The token type.
        expires_in (int): The token ttl.
        refresh_token (str): The refresh token.
        scope (list[str]): The scope.
    '''

    def __init__(
        self,
        access_token: str,
        token_type: str,
        expires_in: int,
        refresh_token: str,
        scope: str,
    ) -> None:
        '''
        The constructor.

        Args:
            access_token (str): The access token.
            token_type (str): The token type.
            expires_in (int): The token ttl.
            refresh_token (str): The refresh token.
            scope (str): The scope.
        '''

        self.access_token: str = access_token
        self.token_type: str = token_type
        self.expires_in: int = expires_in
        self.refresh_token: str = refresh_token

        if ' ' in scope:
            self.scope: list[str] = scope.split()
        else:
            self.scope: list[str] = [scope]

    @property
    def bearer(self) -> str:
        '''
        Returns the bearer token.

        Returns:
            str: The bearer token.
        '''

        return f'Bearer {self.access_token}'

    @property
    def scope_as_str(self) -> str:
        '''
        Returns the scope as a string.

        Returns:
            str: The scope.
        '''

        return ' '.join(self.scope)


class Auth:
    '''
    The Spotify Auth class.
    The authentication process is using OAuth2 protocol.

    Attributes:
        _AUTHORIZE_URL (str): The Spotify authorize url.
        _TOKEN_URL (str): The Spotify token url.
        creds (Credentials): The credentials.
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

        self.creds: Credentials = creds
        self._scope: list[str] = scope
        self._redirect_uri: str = redirect_uri
        self.token: Token = None

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
            'client_id': self.creds.client_id,
            'scope': self._url_encode(self._scope),
            'redirect_uri': self._url_encode(self._redirect_uri),
        }

        return (
            self._AUTHORIZE_URL
            + '?'
            + '&'.join(f'{k}={v}' for k, v in params.items())
        )

    def update_token(self, refresh_token: str) -> Token:
        '''
        Updates the token.
        A refresh token is required to get a new access token.

        Args:
            refresh_token (str): The refresh token.

        Raises:
            TokenRequestError: If the token does not exists
                or if an HTTPError occurs.

        Returns:
            Token: The new token object.
        '''

        if not self.token:
            raise TokenRequestError(
                'An initial token is required before request a refreshed one.'
            )

        headers: dict[str, str] = {
            'Authorization': self.creds.basic,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body: dict[str, str] = {
            'grant_type': 'refresh_token',
            'redirect_uri': self._redirect_uri,
            'refresh_token': self.token.refresh_token,
        }
        response: requests.Response = requests.post(
            self._TOKEN_URL,
            headers=headers,
            data=body,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise TokenRequestError(e)

        json_response: dict[str, str] = response.json()
        self.token.access_token = json_response['access_token']
        self.token.token_type = json_response['token_type']
        self.token.expires_in = json_response['expires_in']
        self.token.scope = json_response['scope'].split()

        return self.token

    def get_token(self, code: str) -> Token:
        '''
        Get access_token from the Spotify Auth Server.

        Args:
            code (str): The authorization code.

        Raises:
            TokenRequestError: If an HTTPError occurs.

        Returns:
            dict[str, str]: The access token.
        '''

        headers: dict[str, str] = {
            'Authorization': self.creds.basic,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body: dict[str, str] = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self._redirect_uri,
        }
        response: requests.Response = requests.post(
            self._TOKEN_URL,
            headers=headers,
            data=body,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise TokenRequestError(e)

        json_response: dict[str, str] = response.json()
        self.token = Token(
            json_response['access_token'],
            json_response['token_type'],
            json_response['expires_in'],
            json_response['refresh_token'],
            json_response['scope'],
        )

        return self.token


class TokenRequestError(Exception):
    ...
