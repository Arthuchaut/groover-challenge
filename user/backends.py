from typing import Union
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from user.models import User


class CustomBackend(BaseBackend):
    '''
    User backend customization.
    '''

    def authenticate(
        self, request: HttpRequest, mail: str
    ) -> Union[User, None]:
        '''
        Redefine the user authentication method.

        Args:
            request (HttpRequest): The request object.
            mail (str): The user mail.

        Returns:
            Union[User, None]: The user object or None.
        '''

        try:
            user: User = User.objects.get(mail=mail)
        except User.DoesNotExist:
            return None

        return user
