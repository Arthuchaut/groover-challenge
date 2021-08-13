from typing import Any, Generator, Iterator, Union
import time
import requests
import pytest
from unittest.mock import Mock
from _pytest.monkeypatch import MonkeyPatch, monkeypatch
from requests.exceptions import HTTPError
from api.libs.spotify.auth import Auth, Token
from api.libs.spotify.spotify_api import SpotifyAPI, SpotifyAPIError


class TestSpotifyAPI:
    @pytest.mark.parametrize(
        'status_code',
        [200, 301, 400, 429, 500],
    )
    def test__get(
        self,
        status_code: int,
        spotify_api: SpotifyAPI,
        monkeypatch: MonkeyPatch,
    ) -> None:
        fake_resp: dict[str, Any] = {'root': {'key': 'value'}}

        class ResponseMock:
            _REQUESTS_COUNT: int = 0

            def __init__(self, *args: Any, **kwargs: Any) -> None:
                if ResponseMock._REQUESTS_COUNT == 0:
                    self.status_code: int = status_code
                else:
                    self.status_code: int = 200

                self.headers: dict[str, str] = {'Retry-After': '0'}
                ResponseMock._REQUESTS_COUNT += 1

            def json(self) -> dict[str, Any]:
                return fake_resp

            def raise_for_status(self) -> None:
                if self.status_code >= 400:
                    raise HTTPError()

        def get_patch(url: str, **kwargs: Any) -> ResponseMock:
            return ResponseMock()

        monkeypatch.setattr(time, 'sleep', Mock())
        monkeypatch.setattr(requests, 'get', get_patch)
        monkeypatch.setattr(requests, 'Response', ResponseMock)
        response: dict[str, Any] = None

        if status_code not in (200, 301, 429):
            with pytest.raises(SpotifyAPIError):
                response = spotify_api._get('fake_resource')
        else:
            response = spotify_api._get('fake_resource')
            assert response == fake_resp

    def test_get_artist(
        self, spotify_api: SpotifyAPI, monkeypatch: MonkeyPatch
    ) -> None:
        fake_resp: Mock = Mock(return_value={'key': 'value'})
        monkeypatch.setattr(spotify_api, '_get', fake_resp)
        response: dict[str, Any] = spotify_api.get_artist(id_='ID')

        assert response == fake_resp.return_value

    @pytest.mark.parametrize(
        'ids',
        [
            ['ID'],
            ['ID'] * 10,
            ['ID'] * 51,
        ],
    )
    def test_get_several_artist(
        self, ids: list[str], spotify_api: SpotifyAPI, monkeypatch: MonkeyPatch
    ) -> None:
        fake_resp: Mock = Mock(return_value={'artists': 'any'})
        monkeypatch.setattr(spotify_api, '_get', fake_resp)
        response: dict[str, Any] = None

        if len(ids) > 50:
            with pytest.raises(SpotifyAPIError):
                response = spotify_api.get_several_artists(ids=ids)
        else:
            response = spotify_api.get_several_artists(ids=ids)
            assert response == 'any'

    def test_get_new_releases(
        self, spotify_api: SpotifyAPI, monkeypatch: MonkeyPatch
    ) -> None:
        fake_resp: Mock = Mock(
            return_value={
                'albums': {
                    'total': 10,
                    'offest': 5,
                    'limit': 5,
                    'items': ['any'],
                }
            }
        )
        monkeypatch.setattr(spotify_api, '_get', fake_resp)
        response: Iterator[dict[str, Any]] = spotify_api.get_new_releases()

        assert isinstance(response, Generator)

    def test_get_me(
        self, spotify_api: SpotifyAPI, monkeypatch: MonkeyPatch
    ) -> None:
        fake_resp: Mock = Mock(return_value={'me': 'any'})
        monkeypatch.setattr(spotify_api, '_get', fake_resp)
        response: dict[str, Any] = spotify_api.get_me()

        assert response == fake_resp.return_value

    def test__raise_for_empty_token(
        self, spotify_api: SpotifyAPI, monkeypatch: MonkeyPatch
    ) -> None:
        spotify_api._raise_for_empty_token()
        spotify_api._auth.token = None

        with pytest.raises(SpotifyAPIError):
            spotify_api._raise_for_empty_token()
