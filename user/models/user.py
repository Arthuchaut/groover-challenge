from datetime import datetime, tzinfo
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import CustomUserManager


class User(AbstractUser):
    '''The custom User model class based on Django default User model.

    Attributes:
        USERNAME_FIELD (str): The username field used for authentication.
        REQUIRED_FIELDS (list[str]): The required nullable fields
            from default model. Empty in our case, cause the email,
            username and password are already required.
        email (models.EmailField): The user email used for authentication.
        refresh_token (models.CharField): The refresh token used for
            refresh acess_token.
        acess_token (models.CharField): The access token used for
            authentication.
        token_type (models.CharField): The token type (e.g. Bearer).
        scope (models.CharField): The scope of accessible resources.
        refreshed_date (models.DateTimeField): The date of last refresh.
        expires_in (models.DateTimeField): The date of acess_token expiration.
        objects (CustomUserManager): The custom User manager class.
    '''

    email: models.EmailField = models.EmailField(unique=True)
    refreshed_date: models.DateTimeField = models.DateTimeField(auto_now=True)
    access_token: models.CharField = models.CharField(max_length=162)
    token_type: models.CharField = models.CharField(max_length=20)
    scope: models.TextField = models.TextField()
    refresh_token: models.CharField = models.CharField(max_length=131)
    expires_in: models.IntegerField = models.IntegerField()

    # Disabled useless fields
    password: None = None
    username: None = None
    first_name: None = None
    last_name: None = None

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    # The custom User manager
    objects: CustomUserManager = CustomUserManager()

    @property
    def token_expired(self) -> bool:
        '''Check if the access_token is expired.

        Returns:
            bool: True if expired, False otherwise.
        '''

        # Compute the difference between
        # the current datetime and the refreshed_date in seconds.
        delta: float = (timezone.now() - self.refreshed_date).total_seconds()

        return delta >= self.expires_in

    @property
    def scope_as_list(self) -> list[str]:
        '''
        Get the scope as a list of strings.
        '''

        return self.scope.split()

    class Meta:
        '''The User meta class definition.

        Attributes:
            app_label (str): The app_label used by Django.
            db_table (str): The database table name overwriting.
        '''

        app_label: str = 'user'
        db_table: str = 'user'
