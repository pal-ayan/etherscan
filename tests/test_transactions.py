import unittest

from src.enums import *
from src.transactions import Transactions


class TestTransactions(unittest.TestCase):
    def setUp(self) -> None:
        self.txn = Transactions()

    def test_exec_status_error(self):
        resp = self.txn.get_contract_exec_status(
            txhash="0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a"
        )
        print(resp)
        self.assertTrue(resp.isError == 1)

    def test_exec_status_success(self):
        resp = self.txn.get_contract_exec_status(
            txhash="0x74cdbc33e60cafe9e8cf51913aea2783502e8db9cd80bc0e2d152723f289d6d9"
        )
        print(resp)
        self.assertTrue(resp.isError == 0)

    def test_receipt_status(self):
        resp = self.txn.get_receipt_status(
            txhash="0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76"
        )
        print(resp)
        self.assertTrue(resp.status == 1)
