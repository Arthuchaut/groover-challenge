from api.models import ArtistImageURL


class TestArtistImageURL:
    def test___str__(self):
        image_url: ArtistImageURL = ArtistImageURL(url='Test')
        assert str(image_url) == 'Test'
