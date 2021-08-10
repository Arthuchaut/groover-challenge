from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Artist


class ArtistExternalURL(models.Model):
    '''
    Model for storing artist external url.

    Attributes:
        external_url_id (models.BigAutoField): Primary key.
        source (models.CharField): Source of the external url.
        url (models.URLField): URL of the external url.
        artist (models.ForeignKey): The related Artist.
    '''

    external_url_id: models.BigAutoField = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False
    )
    source: models.CharField(max_length=150)
    url: models.URLField()
    artist: models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        app_label: str = 'api'
        db_table: str = 'artist_external_url'
        verbose_name: str = _('artist external url')
        verbose_name_plural: str = _('artist external urls')
