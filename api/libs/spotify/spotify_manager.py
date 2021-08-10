from .auth import Auth, Credentials
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
