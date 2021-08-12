from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Genre


class Artist(models.Model):
    '''
    Artist model.

    Attributes:
        artist_id (models.CharField): The Artist ID.
        name (models.CharField): The Artist Name.
        followers (models.IntegerField): The number of followers.
        popularity (models.IntegerField): The popularity of the artist.
        href (models.URLField): The URL of the artist.
        artist_type (models.CharField): The type of the artist.
        uri (models.URLField): The URI of the artist.
        genres (models.ManyToManyField): The genres of the artist.
    '''

    artist_id: models.CharField = models.CharField(
        primary_key=True,
        max_length=22,
        unique=True,
    )
    followers: models.IntegerField = models.IntegerField()
    href: models.URLField = models.URLField()
    name: models.CharField = models.CharField(max_length=255)
    popularity: models.IntegerField = models.IntegerField()
    artist_type: models.CharField = models.CharField(max_length=255)
    uri: models.URLField = models.URLField()
    genres: models.ManyToManyField = models.ManyToManyField(Genre)

    @property
    def as_dict(self) -> dict[str, Any]:
        """
        Format the Artist object in dict object.

        Returns:
            dict[str, Any]: The formatted Artist object.
        """

        return {
            'artist_id': self.artist_id,
            'name': self.name,
            'followers': self.followers,
            'popularity': self.popularity,
            'href': self.href,
            'artist_type': self.artist_type,
            'uri': self.uri,
            'genres': [genre.name for genre in self.genres.all()],
        }

    class Meta:
        app_label: str = 'api'
        db_table: str = 'artist'
        verbose_name: str = _('artist')
        verbose_name_plural: str = _('artists')
