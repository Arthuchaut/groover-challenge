from typing import Any, Union
import requests
import pytest
from unittest.mock import Mock
from _pytest.monkeypatch import MonkeyPatch
from api.libs.spotify.auth import Auth, Token


class TestAuth:
    @pytest.mark.parametrize(
        'obj, expected',
        [
            (
                ['user-read-private', 'user-read-email'],
                'user-read-private%20user-read-email',
            ),
            (
                [
                    'user-read-private',
                    'user-read-email',
                    'user-read-playback-state',
                ],
                'user-read-private%20user-read-email%20user-read-playback-state',
            ),
            (
                'http://localhost:8000/auth/callback/',
                'http%3A//localhost%3A8000/auth/callback/',
            ),
            (
                'http://localhost:8000/auth/callback/?code=abc',
                'http%3A//localhost%3A8000/auth/callback/%3Fcode%3Dabc',
            ),
        ],
    )
    def test__url_encode(
        self, spotify_auth: Auth, obj: Union[list[str], str], expected: str
    ) -> None:
        assert spotify_auth._url_encode(obj) == expected

    def test_authorize_url(self, spotify_auth: Auth) -> None:
        expected: str = (
            'https://accounts.spotify.com/authorize/?'
            'response_type=code&'
            'client_id=CLIENT_ID&'
            'scope=user-read-private%20user-read-email&'
            'redirect_uri=http%3A//localhost%3A8000/auth/callback/'
        )

        assert spotify_auth.authorize_url == expected

    def test_update_token(
        self, spotify_auth: Auth, fake_token: Token, monkeypatch: MonkeyPatch
    ) -> None:
        fake_resp: Mock = Mock()
        fake_resp.return_value.json = lambda: {
            'access_token': 'NEW_ACCESS_TOKEN',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': 'user-read-private user-read-email',
        }
        monkeypatch.setattr(requests, 'post', fake_resp)
        spotify_auth.token = fake_token
        new_token: Token = spotify_auth.update_token(
            refresh_token=fake_token.refresh_token
        )

        assert isinstance(new_token, Token)
        assert new_token.access_token == 'NEW_ACCESS_TOKEN'
        assert spotify_auth.token.access_token == 'NEW_ACCESS_TOKEN'

    def test_get_token(
        self, spotify_auth: Auth, monkeypatch: MonkeyPatch
    ) -> None:
        fake_resp: Mock = Mock()
        fake_resp.return_value.json = lambda: {
            'access_token': 'ACCESS_TOKEN',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': 'REFRESH_TOKEN',
            'scope': 'user-read-private user-read-email',
        }
        monkeypatch.setattr(requests, 'post', fake_resp)

        assert spotify_auth.token == None

        token: Token = spotify_auth.get_token(code='FAKE_CODE')

        assert isinstance(token, Token)
        assert token.access_token == 'ACCESS_TOKEN'
        assert isinstance(spotify_auth.token, Token)
        assert spotify_auth.token.access_token == 'ACCESS_TOKEN'
