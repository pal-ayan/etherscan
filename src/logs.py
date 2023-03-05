from __future__ import annotations

from typing import List

from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, ApiParams, Const, Modules


class EventLogItem(BaseModel):
    address: str
    topics: List[str]
    data: str
    blockNumber: str
    timeStamp: str
    gasPrice: str
    gasUsed: str
    logIndex: str
    transactionHash: str
    transactionIndex: str


class EventLog(BaseModel):
    __root__: List[EventLogItem]


class Logs:
    def get_evt_logs_by_addr(
        self,
        address: str,
        from_block: int,
        to_block: int,
        page: int = 1,
        limit: int = Const.RESP_LENGTH_LIMIT_LOGS.value,
        all_pages: int = 1,
    ) -> EventLog:
        resp = com.get_transactions(
            address=address,
            module=Modules.LOGS,
            action=ApiActions.GETLOGS,
            fromBlock=from_block,
            toBlock=to_block,
            page=page,
            limit=limit,
            all_pages=all_pages,
        )
        return com.generate_model(resp, EventLog)
