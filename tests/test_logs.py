import unittest

import pandas as pd

from src.enums import *
from src.logs import Logs


class TestLogs(unittest.TestCase):
    def setUp(self) -> None:
        self.logs = Logs()

    def test_get_evt_logs_by_addr(self):
        resp = self.logs.get_evt_logs_by_addr(
            address="0xbd3531da5cf5857e7cfaa92426877b022e612cf8",
            from_block=12878196,
            to_block=12878196,
            limit=50,
        )
        print(pd.read_json(resp.json()).info())
        self.assertIsNotNone(resp)
