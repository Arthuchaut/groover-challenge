from django.urls import path
from .views import ArtistView

app_name: str = 'api'
urlpatterns = [
    path('artists/', ArtistView.as_view(), name='artists'),
]
