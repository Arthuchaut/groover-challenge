from api.models.artist_image_url import ArtistImageURL
from api.models.artist_external_url import ArtistExternalURL
from typing import Any
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from api.libs.spotify.spotify_manager import SpotifyManager
from api.models import Album


class ArtistView(View):
    '''
    The /api/artists/ view class.
    '''

    def get(self, request: HttpRequest) -> HttpResponse:
        '''
        The GET method implementation.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A response containing the JSON serialized
                artist list.
        '''

        if not request.user.is_authenticated:
            return redirect('user:auth')

        if request.user.token_expired:
            return redirect('user:auth_refresh_token')

        sp_man: SpotifyManager = SpotifyManager(
            client_id=settings.APP_CONFIG.SPOTIFY_API_CLIENT_ID,
            client_secret=settings.APP_CONFIG.SPOTIFY_API_CLIENT_SECRET,
            scope=settings.APP_CONFIG.SPOTIFY_API_SCOPE,
            redirect_uri=settings.APP_CONFIG.SPOTIFY_API_REDIRECT_URI,
        )
        sp_man.recover_token(request.user)
        new_releases: list[Album] = sp_man.get_new_releases_from_db()
        artists: list[dict[str, Any]] = []

        if not new_releases:
            sp_man.update_new_releases_in_db()
            new_releases = sp_man.get_new_releases_from_db()

        for album in new_releases:
            for artist in album.artists.all():
                external_urls: list[
                    ArtistExternalURL
                ] = ArtistExternalURL.objects.filter(
                    artist__artist_id=artist.artist_id
                )
                image_urls: list[
                    ArtistImageURL
                ] = ArtistImageURL.objects.filter(
                    artist__artist_id=artist.artist_id
                )
                as_dict_artist: dict[str, Any] = artist.as_dict
                as_dict_artist['external_urls'] = []
                as_dict_artist['image_urls'] = []

                for external_url in external_urls:
                    as_dict_artist['external_urls'].append(
                        external_url.as_dict
                    )

                for image_url in image_urls:
                    as_dict_artist['image_urls'].append(image_url.as_dict)

                if not as_dict_artist in artists:
                    artists.append(as_dict_artist)

        return JsonResponse(
            {
                'artists': artists,
            }
        )
