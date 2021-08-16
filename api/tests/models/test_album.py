from api.models import Album


class TestAlbum:
    def test___str__(self):
        album: Album = Album(name='Test')
        assert str(album) == 'Test'
