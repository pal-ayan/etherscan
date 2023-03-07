import unittest

from src.enums import *
from src.tokens import Tokens


class TestTokens(unittest.TestCase):
    def setUp(self) -> None:
        self.tk = Tokens()

    def test_get_balance(self):
        resp = self.tk.get_erc_20_toke_acc_bal(
            contract_address="0x57d90b64a1a57749b0f932f1a3395792e12e7055",
            address="0xe04f27eb70e025b78871a2ad7eabe85e61212761",
        )
        print(resp)
        self.assertIsInstance(resp, int)

    def test_get_supply(self):
        resp = self.tk.get_erc_20_total_token_supply(
            contract_address="0x57d90b64a1a57749b0f932f1a3395792e12e7055"
        )
        print(resp)
        self.assertIsInstance(resp, int)
