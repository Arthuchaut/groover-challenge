from api.models import Genre


class TestGenre:
    def test___str__(self):
        genre: Genre = Genre(name='Test')
        assert str(genre) == 'Test'
