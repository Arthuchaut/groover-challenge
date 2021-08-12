from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    '''
    The custom User manager class.
    '''

    def create_or_update_user(
        self,
        email: str,
        access_token: str,
        token_type: str,
        scope: str,
        expires_in: int,
        refresh_token: str = None,
    ) -> object:
        '''
        Creates and saves a User with the given email, access_token,
        token_type, scope, refresh_token, and expires_in.

        Args:
            email (str): The email of the user.
            access_token (str): The access token of the user.
            token_type (str): The token type of the user.
            scope (str): The scope of the user.
            expires_in (int): The expiration time of the user.
            refresh_token (str): The refresh token of the user.
                Default to None.

        Raises:
            ValueError: If a required arg is not provided.

        Returns:
            User: The user model.
        '''

        ignored_params: list[str] = ['refresh_token']

        for attr, val in locals().items():
            if not attr in ignored_params and not val:
                raise ValueError(f'Missing {attr} parameter.')

        try:
            user: self.model = self.model.objects.get(
                email=self.normalize_email(email)
            )
            user.access_token = access_token
            user.token_type = token_type
            user.scope = scope
            user.expires_in = expires_in

            if refresh_token:
                user.refresh_token = refresh_token
        except self.model.DoesNotExist:
            user = self.model(
                email=self.normalize_email(email),
                access_token=access_token,
                token_type=token_type,
                scope=scope,
                refresh_token=refresh_token,
                expires_in=expires_in,
            )

        user.save(using=self._db)

        return user
