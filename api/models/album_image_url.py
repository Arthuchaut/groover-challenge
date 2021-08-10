from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Album


class AlbumImageURL(models.Model):
    '''
    Model representing an image url for an album.

    Attributes:
        image_url_id (models.BigAutoField): The primary key.
        width (models.IntegerField): The width of the image.
        height (models.IntegerField): The height of the image.
        url (models.URLField): The url of the image.
        album (models.ForeignKey): The related album.
    '''

    image_url_id: models.BigAutoField = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False
    )
    width: models.IntegerField = models.IntegerField()
    height: models.IntegerField = models.IntegerField()
    url: models.URLField = models.URLField()
    album: models.ForeignKey = models.ForeignKey(
        Album, on_delete=models.CASCADE
    )

    class Meta:
        app_label: str = 'api'
        db_table: str = 'album_image_url'
        verbose_name: str = _('album image url')
        verbose_name_plural: str = _('album image urls')
