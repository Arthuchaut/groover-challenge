from api.libs.spotify.spotify_api import SpotifyAPIError
from django.http.response import (
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login
from user.models import User
from api.libs.spotify.spotify_manager import SpotifyManager
from api.libs.spotify.auth import Token, TokenRequestError
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
            _(f'User already authenticated with {request.user.email}.')
        )


class AuthRefreshTokenView(View):
    '''
    The /auth/refresh-token class.
    '''

    def get(self, request: HttpRequest) -> HttpResponse:
        '''
        The GET method implementation.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: An HTTP response.
        '''

        if not request.user.is_authenticated:
            return redirect('user:auth')

        sp_man: SpotifyManager = SpotifyManager(
            client_id=settings.APP_CONFIG.SPOTIFY_API_CLIENT_ID,
            client_secret=settings.APP_CONFIG.SPOTIFY_API_CLIENT_SECRET,
            scope=settings.APP_CONFIG.SPOTIFY_API_SCOPE,
            redirect_uri=settings.APP_CONFIG.SPOTIFY_API_REDIRECT_URI,
        )
        sp_man.recover_token(request.user)

        try:
            sp_man.auth.update_token(request.user.refresh_token)
        except TokenRequestError as e:
            return HttpResponseBadRequest(e)

        User.objects.create_or_update_user(
            email=request.user.email,
            access_token=sp_man.auth.token.access_token,
            token_type=sp_man.auth.token.token_type,
            refresh_token=sp_man.auth.token.refresh_token,
            scope=sp_man.auth.token.scope_as_str,
            expires_in=sp_man.auth.token.expires_in,
        )

        return redirect('api:artists')


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

        sp_man: SpotifyManager = SpotifyManager(
            client_id=settings.APP_CONFIG.SPOTIFY_API_CLIENT_ID,
            client_secret=settings.APP_CONFIG.SPOTIFY_API_CLIENT_SECRET,
            scope=settings.APP_CONFIG.SPOTIFY_API_SCOPE,
            redirect_uri=settings.APP_CONFIG.SPOTIFY_API_REDIRECT_URI,
        )
        code: str = request.GET.get('code')

        if not code:
            return HttpResponseBadRequest(_('Missing code.'))

        try:
            token_info: dict[str, str] = sp_man.auth.get_token(code)
            me_info: dict[str, str] = sp_man.api.get_me()
        except (TokenRequestError, SpotifyAPIError) as e:
            return HttpResponseServerError(e)

        user: User = User.objects.create_or_update_user(
            email=me_info['email'],
            access_token=token_info.access_token,
            token_type=token_info.token_type,
            refresh_token=token_info.refresh_token,
            expires_in=token_info.expires_in,
            scope=token_info.scope_as_str,
        )
        login(request, user)

        return redirect('api:artists')
