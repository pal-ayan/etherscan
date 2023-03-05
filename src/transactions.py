import json

from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, Modules


class ExecStatus(BaseModel):
    isError: int
    errDescription: str


class ReceiptStatus(BaseModel):
    status: int


class Transactions:
    def get_contract_exec_status(self, txhash: str) -> ExecStatus:
        resp = com.get_transactions(
            hash=txhash, module=Modules.TRANSACTION, action=ApiActions.GETSTATUS
        )
        return com.generate_model(resp, ExecStatus)

    def get_receipt_status(self, txhash: str) -> ReceiptStatus:
        resp = com.get_transactions(
            hash=txhash,
            module=Modules.TRANSACTION,
            action=ApiActions.GETTXRECEIPTSTATUS,
        )
        return com.generate_model(resp, ReceiptStatus)
