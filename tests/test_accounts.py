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

    def test_get_balance(self):
        bal = self.acc.get_balance(
            "0x4AB1BF59F3802f8CD78f9CE488D6778Eac12bAA9",
            AccountsTags.LATEST,
        )
        print(bal)
        self.assertIsNotNone(bal)

    def test_get_normal_txns(self):
        ret = self.acc.get_normal_transactions(
            address="0x4AB1BF59F3802f8CD78f9CE488D6778Eac12bAA9",
            sort_order=Const.SORT_ASC,
            limit=Const.RESP_LENGTH_LIMIT.value,
        )
        print(ret)
        self.assertIsNotNone(ret)

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
