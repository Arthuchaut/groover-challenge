from django.db import models
from django.utils.translation import gettext_lazy as _


class Genre(models.Model):
    '''
    Genre model

    Args:
        genre_id (models.BigAutoField): The Genre ID.
        name (models.CharField): The Genre name.
    '''

    genre_id: models.BigAutoField = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False
    )
    name: models.CharField = models.CharField(max_length=150)

    class Meta:
        app_label: str = 'genre'
        db_table: str = 'genre'
        verbose_name: str = _('genre')
        verbose_name_plural: str = _('genres')
