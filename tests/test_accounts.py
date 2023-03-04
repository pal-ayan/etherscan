import unittest

from dotenv import load_dotenv

from src.accounts import Accounts
from src.enums import *

# from . import accounts as accounts
# from . import enums as enums

load_dotenv()


class TestAccounts(unittest.TestCase):
    def setUp(self) -> None:
        self.acc = Accounts()

    @unittest.skip
    def test_get_balance(self):
        bal = self.acc.get_balance(
            "0x4AB1BF59F3802f8CD78f9CE488D6778Eac12bAA9",
            AccountsTags.LATEST,
        )
        print(bal)
        self.assertIsNotNone(bal)

    @unittest.skip
    def test_get_normal_txns(self):
        ret = self.acc.get_normal_transactions(
            address="0x4AB1BF59F3802f8CD78f9CE488D6778Eac12bAA9",
            sort_order=Const.SORT_ASC,
            limit=Const.RESP_LENGTH_LIMIT.value,
        )
        print(ret.json())
        self.assertIsNotNone(ret)

    @unittest.skip
    def test_get_erc20_token_trnsfr_evnt(self):
        ret = self.acc.get_erc20_token_transfer_events(
            # address=None,
            address="0x4e83362442b8d1bec281594cea3050c8eb01311c",
            # contract_address=None,
            contract_address="0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
            limit=100,
            page=0,
        )
        print(ret)
        self.assertIsNotNone(ret)

    @unittest.skip
    def test_get_internal_txn_by_hash(self):
        ret = self.acc.get_internal_transactions_by_hash(
            txhash="0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170"
        )
        # print(ret.json())
        self.assertIsNotNone(ret)

    @unittest.skip
    def test_get_internal_transactions_by_address(self):
        ret = self.acc.get_internal_transactions_by_address(
            address="0x2c1ba59d6f58433fb1eaee7d20b26ed83bda51a3"
        )
        # print(ret.json())
        self.assertIsNotNone(ret)

    @unittest.skip
    def test_get_internal_transactions_by_block_range(self):
        ret = self.acc.get_internal_transactions_by_block_range(
            start_block=13481773, end_block=13491773
        )
        # print(ret.json())
        self.assertIsNotNone(ret)

    @unittest.skip
    def test_get_erc20_token_transfer_events(self):
        ret = self.acc.get_erc20_token_transfer_events(
            contract_address="0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
            address="0x4e83362442b8d1bec281594cea3050c8eb01311c",
            limit=1,
            page=1,
        )
        self.assertIsNotNone(ret)

    # @unittest.skip
    def test_get_erc721(self):
        ret = self.acc.get_erc721_token_transfer_events(
            contract_address="0x06012c8cf97bead5deae237070f9587f8e7a266d",
            address="0x6975be450864c02b4613023c2152ee0743572325",
            limit=2,
            page=1,
        )
        self.assertIsNotNone(ret)

    def test_get_erc1155(self):
        ret = self.acc.get_erc1155_token_transfer_events(
            contract_address="0x76be3b62873462d2142405439777e971754e8e77",
            address="0x83f564d180b58ad9a02a449105568189ee7de8cb",
            limit=2,
            page=1,
        )
        self.assertIsNotNone(ret)

    def test_get_blocks_mined(self):
        ret = self.acc.get_blocks_mined_by_address(
            address="0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b",
            limit=2,
            page=1,
        )
        self.assertIsNotNone(ret)
