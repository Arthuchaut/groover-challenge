from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Market, Artist


class Album(models.Model):
    '''
    Album model.

    Attributes:
        artist_id (models.CharField): The Artist id.
        album_type (models.CharField): The album type.
        href (models.URLField): The album href.
        name (models.CharField): The album name.
        release_date (models.DateField): The album release date.
        last_checked_date (models.DateField): The last checked date.
        release_date_precision (models.CharField): The release date precision.
        total_track (models.IntegerField): The total track.
        other_album_type (models.CharField): The other album type.
        uri (models.URLField): The album uri.
        available_markets (models.ManyToManyField): The available markets.
    '''

    album_id: models.CharField = models.CharField(
        primary_key=True,
        max_length=22,
        unique=True,
    )
    album_type: models.CharField = models.CharField(max_length=50)
    href: models.URLField = models.URLField()
    name: models.CharField = models.CharField(max_length=150)
    release_date: models.DateField = models.DateField()
    last_checked_date: models.DateField = models.DateField()
    release_date_precision: models.CharField = models.CharField(max_length=10)
    total_tracks: models.IntegerField = models.IntegerField()
    other_album_type: models.CharField = models.CharField(max_length=50)
    uri: models.URLField = models.URLField()
    available_markets: models.ManyToManyField = models.ManyToManyField(
        Market, related_name='album', blank=True, db_table='available_markets'
    )
    artists: models.ManyToManyField = models.ManyToManyField(
        Artist, related_name='album', blank=True, db_table='artists_albums'
    )

    class Meta:
        app_label: str = 'api'
        db_table: str = 'album'
        verbose_name: str = _('album')
        verbose_name_plural: str = _('albums')
