from typing import Any, Iterator
from django.utils import timezone
from user.models import User
from .auth import Auth, Credentials, Token
from .spotify_api import SpotifyAPI
from api.models import (
    Album,
    AlbumImageURL,
    AlbumExternalURL,
    Artist,
    ArtistImageURL,
    ArtistExternalURL,
    Genre,
    Market,
)


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

    def recover_token(self, user: User) -> None:
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

    def get_today_new_releases(self) -> list[Album]:
        '''
        Get the new releases from the database.
        Filter the query by the current date.
        If no data is found, update DB from Spotify API
        and return the new releases.

        Returns:
            list[Album]: The list of new releases.
        '''

        today_releases: list[Album] = Album.objects.filter(
            last_checked_date=timezone.now()
        )

        if not today_releases:
            today_releases = self.update_new_releases_in_db()

        return today_releases

    def _update_artists_in_db(self, artist_ids: list[str]) -> set[Artist]:
        '''
        Update the artists in the database.

        Args:
            artist_ids (list[str]): The list of artist ids.

        Returns:
            set[Artist]: The set of artists.
        '''

        artists_info: dict[str, Any] = self.api.get_several_artists(
            ids=artist_ids
        )
        artist_set: set[Artist] = set()

        for artist_info in artists_info:
            genre_set: set[Genre] = set()
            artist_model, _ = Artist.objects.get_or_create(
                artist_id=artist_info['id'],
                name=artist_info['name'],
                followers=artist_info['followers']['total'],
                popularity=artist_info['popularity'],
                artist_type=artist_info['type'],
                uri=artist_info['uri'],
                href=artist_info['href'],
            )

            for genre in artist_info['genres']:
                genre_model, _ = Genre.objects.get_or_create(name=genre)
                genre_set.add(genre_model)

            for source, url in artist_info['external_urls'].items():
                ArtistExternalURL.objects.update_or_create(
                    source=source,
                    url=url,
                    artist_id=artist_model.artist_id,
                )

            for image_url in artist_info['images']:
                ArtistImageURL.objects.update_or_create(
                    width=image_url['width'],
                    height=image_url['height'],
                    url=image_url['url'],
                    artist_id=artist_model.artist_id,
                )

            artist_model.genres.add(*genre_set)
            artist_set.add(artist_model)

        return artist_set

    def _update_album_in_db(self, album_info: dict[str, Any]) -> Album:
        '''
        Create or update the album in the database.
        If the album already exists, update the last_checked_date field.

        Args:
            album_info (dict[str, Any]): The album info.

        Returns:
            Album: The album created/updated.
        '''

        market_set: set[Market] = set()

        try:
            album_model: Album = Album.objects.get(album_id=album_info['id'])
            album_model.last_checked_date = timezone.now()
            album_model.save()
        except Album.DoesNotExist:
            album_model, _ = Album.objects.create(
                album_id=album_info['id'],
                album_type=album_info['album_type'],
                name=album_info['name'],
                release_date=album_info['release_date'],
                release_date_precision=album_info['release_date_precision'],
                last_checked_date=timezone.now(),
                object_type=album_info['type'],
                uri=album_info['uri'],
                href=album_info['href'],
            )

        for country_code in album_info['available_markets']:
            (
                market_model,
                _,
            ) = Market.objects.get_or_create(country_code=country_code)
            market_set.add(market_model)

        for source, url in album_info['external_urls'].items():
            AlbumExternalURL.objects.update_or_create(
                source=source,
                url=url,
                album_id=album_model.album_id,
            )

        for image_url in album_info['images']:
            AlbumImageURL.objects.update_or_create(
                width=image_url['width'],
                height=image_url['height'],
                url=image_url['url'],
                album_id=album_model.album_id,
            )

        album_model.available_markets.add(*market_set)

        return album_model

    def update_new_releases_in_db(self) -> list[Album]:
        '''
        Update the new releases in the database.
        '''

        new_releases: Iterator[dict[str, Any]] = self.api.get_new_releases()
        albums: list[Album] = []

        for album_info in new_releases:
            artist_ids: list[str] = [
                artist['id'] for artist in album_info['artists']
            ]
            artist_set: set[Artist] = self._update_artists_in_db(artist_ids)
            album_model: Album = self._update_album_in_db(album_info)
            album_model.artists.add(*artist_set)
            albums.append(album_model)

        return albums
