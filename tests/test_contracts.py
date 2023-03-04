import unittest

from dotenv import load_dotenv

from src.contracts import Contracts
from src.enums import *

# from . import accounts as accounts
# from . import enums as enums

load_dotenv()


class TestContracts(unittest.TestCase):
    def setUp(self) -> None:
        self.con = Contracts()

    def test_abi(self):
        df = self.con.get_abi_for_verified_contract_src_code(
            address="0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413"
        )
        print(df.head(57))
        self.assertIsNotNone(df)
