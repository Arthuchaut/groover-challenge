from api.models import AlbumImageURL


class TestAlbumImageURL:
    def test___str__(self):
        image_url: AlbumImageURL = AlbumImageURL(url='Test')
        assert str(image_url) == 'Test'
