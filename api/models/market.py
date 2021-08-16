from django.db import models
from django.utils.translation import gettext_lazy as _


class Market(models.Model):
    '''
    The market model.

    Attributes:
        market_id (models.BigAutoField): The market id.
        country_code (models.CharField): The country code.
    '''

    market_id: models.BigAutoField = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False
    )
    country_code: models.CharField = models.CharField(max_length=2)

    def __str__(self) -> str:
        return self.country_code

    class Meta:
        app_label: str = 'api'
        db_table: str = 'market'
        verbose_name: str = _('market')
        verbose_name_plural: str = _('markets')
