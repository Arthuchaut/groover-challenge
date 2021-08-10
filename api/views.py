from user.models import user
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from api.libs.spotify.spotify_manager import SpotifyManager
from django.conf import settings


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

        return HttpResponse('Artists view not implemented yet.')
