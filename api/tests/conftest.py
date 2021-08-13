import pytest
from api.libs.spotify.auth import Auth, Credentials, Token
from api.libs.spotify.spotify_api import SpotifyAPI


@pytest.fixture
def fake_token() -> Token:
    return Token(
        access_token='ACCESS_TOKEN',
        expires_in=3600,
        refresh_token='REFRESH_TOKEN',
        scope='user-read-private user-read-email',
        token_type='Bearer',
    )


@pytest.fixture
def spotify_auth() -> Auth:
    creds: Credentials = Credentials(
        client_id='CLIENT_ID',
        client_secret='CLIENT_SECRET',
    )
    return Auth(
        creds,
        scope=['user-read-private', 'user-read-email'],
        redirect_uri='http://localhost:8000/auth/callback/',
    )


@pytest.fixture
def spotify_api(spotify_auth: Auth, fake_token: Token) -> SpotifyAPI:
    spotify_auth.token = fake_token
    return SpotifyAPI(auth=spotify_auth)
