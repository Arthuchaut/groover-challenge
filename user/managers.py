from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    '''
    The custom User manager class.
    '''

    def create_user(
        self,
        email: str,
        access_token: str,
        token_type: str,
        scope: str,
        refresh_token: str,
        expires_in: int,
    ) -> object:
        '''
        Creates and saves a User with the given email, access_token,
        token_type, scope, refresh_token, and expires_in.

        Args:
            email (str): The email of the user.
            access_token (str): The access token of the user.
            token_type (str): The token type of the user.
            scope (str): The scope of the user.
            refresh_token (str): The refresh token of the user.
            expires_in (int): The expiration time of the user.

        Returns:
            User: The user model.
        '''
        for attr, val in locals().items():
            if not val:
                raise ValueError(f'Missing {attr} parameter.')

        user: self.model = self.model(
            email=self.normalize_email(email),
            access_token=access_token,
            token_type=token_type,
            scope=scope,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )
        user.save(using=self._db)

        return user
