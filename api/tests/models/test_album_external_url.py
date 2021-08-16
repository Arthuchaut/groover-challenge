from api.models import AlbumExternalURL


class TestAlbumExternalURL:
    def test___str__(self):
        external_url: AlbumExternalURL = AlbumExternalURL(url='Test')
        assert str(external_url) == 'Test'
