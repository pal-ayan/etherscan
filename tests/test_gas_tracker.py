import unittest

from src.enums import *
from src.gas_tracker import GasTracker


class TestGasTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.gt = GasTracker()

    def test_get_conf_time_estimate(self):
        resp = self.gt.get_estimated_conf_time(gas_price=2000000000)
        print(resp)
        self.assertIsInstance(resp, int)

    def test_get_gas_oracle(self):
        resp = self.gt.get_gas_oracle()
        print(resp)
        self.assertIsNotNone(resp)
