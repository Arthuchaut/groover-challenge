from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Artist


class ArtistImageURL(models.Model):
    '''
    Model representing an image url for an artist.

    Attributes:
        image_url_id (models.BigAutoField): The primary key.
        width (models.IntegerField): The width of the image.
        height (models.IntegerField): The height of the image.
        url (models.URLField): The url of the image.
        artist (models.ForeignKey): The related artist.
    '''

    image_url_id: models.BigAutoField = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False
    )
    width: models.IntegerField = models.IntegerField()
    height: models.IntegerField = models.IntegerField()
    url: models.URLField = models.URLField()
    artist: models.ForeignKey = models.ForeignKey(
        Artist, on_delete=models.CASCADE
    )

    class Meta:
        app_label: str = 'api'
        db_table: str = 'artist_image_url'
        verbose_name: str = _('artist image url')
        verbose_name_plural: str = _('artist image urls')
