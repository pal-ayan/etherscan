from __future__ import annotations

import datetime
from typing import List, Literal, Union

from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, Const, Modules


class ETH2(BaseModel):
    EthSupply: int
    Eth2Staking: int
    BurntFees: int


class ETHPrice(BaseModel):
    ethbtc: float
    ethbtc_timestamp: datetime.datetime
    ethusd: float
    ethusd_timestamp: datetime.datetime


class NodeCount(BaseModel):
    UTCDate: datetime.date
    TotalNodeCount: int


class NodeSizeItem(BaseModel):
    blockNumber: int
    chainTimeStamp: datetime.date
    chainSize: int
    clientType: str
    syncMode: str


class EthNodeSize(BaseModel):
    __root__: List[NodeSizeItem]


class Stats:
    def get_total_ether_supply(self) -> Union[None, int]:
        resp = com.get_transactions(
            module=Modules.STATS, action=ApiActions.ETHSUPPLY
        )

        if resp is None:
            return None
        try:
            return int(resp)
        except TypeError:
            return None

    def get_total_ether2_supply(self) -> Union[None, ETH2]:
        return com.generate_model(
            com.get_transactions(
                module=Modules.STATS, action=ApiActions.ETHSUPPLY2
            ),
            ETH2,
        )

    def get_ether_last_price(self) -> Union[None, ETHPrice]:
        return com.generate_model(
            com.get_transactions(
                module=Modules.STATS, action=ApiActions.ETHPRICE
            ),
            ETHPrice,
        )

    def get_total_nodes_count(self) -> Union[None, NodeCount]:
        return com.generate_model(
            com.get_transactions(
                module=Modules.STATS, action=ApiActions.NODECOUNT
            ),
            NodeCount,
        )

    def get_eth_nodes_size(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        client_type: Literal[Const.CLIENTTYPE_GETH, Const.CLIENTTYPE_PARITY],
        sort: Literal[Const.SORT_ASC, Const.SORT_DESC],
        sync_mode: Literal[Const.SYNCMODE_ARCHIVE, Const.SYNCMODE_DEFAULT],
    ) -> Union[None, EthNodeSize]:
        return com.generate_model(
            com.get_transactions(
                module=Modules.STATS,
                action=ApiActions.CHAINSIZE,
                start_date=start_date,
                end_date=end_date,
                client_type=client_type,
                sort_order=sort,
                sync_mode=sync_mode,
            ),
            EthNodeSize,
        )
