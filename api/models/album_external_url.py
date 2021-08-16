from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Album


class AlbumExternalURL(models.Model):
    '''
    Model for storing album external url.

    Attributes:
        external_url_id (models.BigAutoField): Primary key.
        source (models.CharField): Source of the external url.
        url (models.URLField): URL of the external url.
        album (models.ForeignKey): The related Album.
    '''

    external_url_id: models.BigAutoField = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False
    )
    source: models.CharField = models.CharField(max_length=150)
    url: models.URLField = models.URLField()
    album: models.ForeignKey = models.ForeignKey(
        Album, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.url

    class Meta:
        app_label: str = 'api'
        db_table: str = 'album_external_url'
        verbose_name: str = _('album external url')
        verbose_name_plural: str = _('album external urls')
