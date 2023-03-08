from __future__ import annotations

import datetime
from typing import Union

from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, Modules


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
