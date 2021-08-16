import pytest
from api.models import ArtistExternalURL, Artist


class TestArtistExternalURL:
    def test___str__(self):
        external_url: ArtistExternalURL = ArtistExternalURL(url='Test')
        assert str(external_url) == 'Test'

    @pytest.mark.django_db
    def test_as_dict(self):
        artist: Artist = Artist.objects.create(
            artist_id='id',
            name='name',
            followers=10,
            href='https://url.test',
            popularity=10,
            artist_type='artist_type',
            uri='uri',
        )
        external_url: ArtistExternalURL = ArtistExternalURL.objects.create(
            source='source', url='url', artist=artist
        )

        assert external_url.as_dict == {
            'id': external_url.external_url_id,
            'source': external_url.source,
            'url': external_url.url,
        }
