import datetime
import unittest

from src.enums import Const
from src.stats import Stats


class TestStats(unittest.TestCase):
    def setUp(self) -> None:
        self.sts = Stats()

    @unittest.skip
    def test_total_eth_supply(self):
        resp = self.sts.get_total_ether_supply()
        print(resp)
        self.assertIsInstance(resp, int)

    @unittest.skip
    def test_total_eth2_supply(self):
        resp = self.sts.get_total_ether2_supply()
        print(resp)
        self.assertIsNotNone(resp, int)

    @unittest.skip
    def test_eth_last_price(self):
        resp = self.sts.get_ether_last_price()
        print(resp.json())
        self.assertIsNotNone(resp)

    @unittest.skip
    def test_total_nodes_count(self):
        resp = self.sts.get_total_nodes_count()
        print(resp.json())
        self.assertIsNotNone(resp.json())

    def test_nodes_size(self):
        resp = self.sts.get_eth_nodes_size(
            start_date=datetime.date(year=2019, month=2, day=1),
            end_date=datetime.date(year=2019, month=2, day=28),
            client_type=Const.CLIENTTYPE_GETH,
            sync_mode=Const.SYNCMODE_DEFAULT,
            sort=Const.SORT_ASC,
        )
        print(resp.json())
        self.assertIsNotNone(resp.json())
