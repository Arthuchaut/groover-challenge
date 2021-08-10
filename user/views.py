from django.http.response import HttpResponseBadRequest
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from api.libs.spotify.spotify_manager import SpotifyManager
from django.conf import settings


class AuthView(View):
    '''
    The /auth view class.
    '''

    def get(self, request: HttpRequest) -> HttpResponse:
        '''
        The GET method implementation.
        If the user is not authenticated, redirect it
        to the Spotify Auth Server.
        Else, send a 400 Bad Request response.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: An HTTP response.
        '''

        if not request.user.is_authenticated:
            sp_man: SpotifyManager = SpotifyManager(
                client_id=settings.APP_CONFIG.SPOTIFY_API_CLIENT_ID,
                client_secret=settings.APP_CONFIG.SPOTIFY_API_CLIENT_SECRET,
                scope=settings.APP_CONFIG.SPOTIFY_API_SCOPE,
                redirect_uri=settings.APP_CONFIG.SPOTIFY_API_REDIRECT_URI,
            )
            return redirect(sp_man.auth.authorize_url)

        return HttpResponseBadRequest(
            _(f'User already authenticated with {request.user.mail}.')
        )


class AuthCallbackView(View):
    '''
    The /auth/callback view class.
    '''

    def get(self, request: HttpRequest) -> HttpResponse:
        '''
        The GET method implementation.
        Request the Spotify Token and create a new user,
        then authenticate it.
        Reidrect the client to the /api/artists route.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: An HTTP response.
        '''

        code: str = request.GET.get('code')

        # TODO: User creation/updating process.

        return HttpResponse('Redirection not implemented yet.')
