import pytest
from api.models import Artist, Genre


class TestArtist:
    def test___str__(self):
        artist: Artist = Artist(name='Test')
        assert str(artist) == 'Test'

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
        artist.genres.set(
            [
                Genre.objects.create(name='genre1'),
                Genre.objects.create(name='genre2'),
            ]
        )
        assert artist.as_dict == {
            'artist_id': artist.artist_id,
            'name': artist.name,
            'followers': artist.followers,
            'popularity': artist.popularity,
            'href': artist.href,
            'artist_type': artist.artist_type,
            'uri': artist.uri,
            'genres': [genre.name for genre in artist.genres.all()],
        }
