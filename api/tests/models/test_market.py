from api.models import Market


class TestMarket:
    def test___str__(self):
        market: Market = Market(country_code='EN')
        assert str(market) == 'EN'
