import os
from dataclasses import dataclass, field


@dataclass
class Config:
    '''
    Configuration class for core.

    Attributes:
        SPOTIFY_API_REDIRECT_URI (str): The Spotify API redirect URI.
        SPOTIFY_API_SCOPE (list[str]): The Spotify API scope.
        SPOTIFY_API_CLIENT_ID (str): The Spotify API client ID.
        SPOTIFY_API_CLIENT_SECRET (str): The Spotify API client secret.
        POSTGRES_HOST (str): The PostgreSQL host.
        POSTGRES_PORT (int): The PostgreSQL port.
        POSTGRES_USER (str): The PostgreSQL user.
        POSTGRES_PASS (str): The PostgreSQL password.
    '''

    SPOTIFY_API_REDIRECT_URI: str = os.environ['SPOTIFY_API_REDIRECT_URI']
    SPOTIFY_API_SCOPE: list[str] = field(
        default_factory=os.environ['SPOTIFY_API_SCOPE'].split
    )
    SPOTIFY_API_CLIENT_ID: str = os.environ['SPOTIFY_API_CLIENT_ID']
    SPOTIFY_API_CLIENT_SECRET: str = os.environ['SPOTIFY_API_CLIENT_SECRET']
    POSTGRES_HOST: str = os.environ['POSTGRES_HOST']
    POSTGRES_PORT: int = int(os.environ['POSTGRES_PORT'])
    POSTGRES_USER: str = os.environ['POSTGRES_USER']
    POSTGRES_PASS: str = os.environ['POSTGRES_PASS']
