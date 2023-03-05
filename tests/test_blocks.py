import unittest

from src.blocks import Blocks
from src.enums import *


class TestBlocks(unittest.TestCase):
    def setUp(self) -> None:
        self.blk = Blocks()

    @unittest.skip
    def test_get_reward(self):
        resp = self.blk.get_block_and_uncle_rewards(block_number=2165403)
        print(resp)
        self.assertIsNotNone(resp)

    @unittest.skip
    def test_get_countdown(self):
        resp = self.blk.get_estimated_blck_countdown(block_number=16761914)
        print(resp)
        self.assertIsNotNone(resp)

    def test_get_blk_num_by_ts(self):
        resp = self.blk.get_block_number_by_ts(timestamp=1578638524)
        print(resp)
        self.assertIsNotNone(resp)
