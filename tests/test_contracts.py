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
        model = self.con.get_abi_for_verified_contract_src_code(
            address="0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413"
        )
        print(model.json())
        self.assertIsNotNone(model)

    def test_src_code(self):
        model, src_code = self.con.get_src_code_for_vc_src_code(
            address="0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413"
        )
        print(model.json())
        self.assertIsNotNone(model)

    def test_creator(self):
        model = self.con.get_creator_data(
            contract_addresses=[
                "0xB83c27805aAcA5C7082eB45C868d955Cf04C337F",
                "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
                "0xe4462eb568E2DFbb5b0cA2D3DbB1A35C9Aa98aad",
                "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "0xf5b969064b91869fBF676ecAbcCd1c5563F591d0",
            ]
        )
        print(model.json())
        self.assertIsNotNone(model)
