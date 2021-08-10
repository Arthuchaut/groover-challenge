from user.models import User
from .auth import Auth, Credentials, Token
from .spotify_api import SpotifyAPI


class SpotifyManager:
    '''
    This class allow to use the Spotify API in a simplified way.

    Attributes:
        auth (Auth): The Spotify Auth object.
        api (SpotifyAPI): The Spotify API object.
    '''

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scope: list[str],
        redirect_uri: str,
    ):
        '''
        The constructor.

        Args:
            client_id (str): The client id.
            client_secret (str): The client secret.
            scope (list[str]): The scope.
            redirect_uri (str): The redirect uri.
        '''

        self.auth: Auth = Auth(
            Credentials(client_id, client_secret),
            scope=scope,
            redirect_uri=redirect_uri,
        )
        self.api: SpotifyAPI = SpotifyAPI(self.auth)

    def init_token(self, user: User) -> None:
        '''
        Initialize the token from the user.

        Args:
            user (User): The user.
        '''

        self.auth.token = Token(
            access_token=user.access_token,
            token_type=user.token_type,
            refresh_token=user.refresh_token,
            expires_in=user.expires_in,
            scope=user.scope,
        )
