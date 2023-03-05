from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, Const, Modules


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
    ) -> Union[None, EventLog]:
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

    def get_evt_logs_by_addr_filtered_by_topic(
        self,
        from_block: int,
        to_block: int,
        address: str,
        topic0: str,
        topic1: str,
        topic2: str,
        topic3: str,
        operator: Optional[Dict[str, list[str]]] = None,
    ):

        """
        operator

            example: {
                'and': [topic1, topic2],
                'or': [topic2, topic3]
            }

            caution:    please use combination of operators at your onw risk.
                        combining operators over multiple topics will result
                        in unexpected responses for example topic 0
                        and (topic 2 or 3) will yeild a different result
                        than topic 1 and (topic 3 or 2), so for some odd
                        reason the sequence also matters.
        """

        # self._validate_operator(operator)
        # operators: list = self._generate_operator(operator)
