from django.db import models
from django.utils.translation import gettext_lazy as _


class Genre(models.Model):
    '''
    Genre model

    Attributes:
        genre_id (models.BigAutoField): The Genre ID.
        name (models.CharField): The Genre name.
    '''

    genre_id: models.BigAutoField = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False
    )
    name: models.CharField = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        app_label: str = 'api'
        db_table: str = 'genre'
        verbose_name: str = _('genre')
        verbose_name_plural: str = _('genres')
