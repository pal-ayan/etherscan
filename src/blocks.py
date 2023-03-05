from typing import List

from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, Const, Modules


class BlockCountDown(BaseModel):
    CurrentBlock: int
    CountdownBlock: int
    RemainingBlock: int
    EstimateTimeInSec: float


class Uncle(BaseModel):
    miner: str
    unclePosition: int
    blockreward: int


class Rewards(BaseModel):
    blockNumber: int
    timeStamp: int
    blockMiner: str
    blockReward: int
    uncles: List[Uncle]
    uncleInclusionReward: int


class Blocks:
    def get_block_and_uncle_rewards(self, block_number: int) -> Rewards:
        resp = com.get_transactions(
            module=Modules.BLOCK,
            action=ApiActions.GETBLOCKREWARD,
            block_number=block_number,
        )
        return com.generate_model(resp, Rewards)

    def get_estimated_blck_countdown(self, block_number: int) -> BlockCountDown:
        resp = com.get_transactions(
            module=Modules.BLOCK,
            action=ApiActions.GETBLOCKCOUNTDOWN,
            block_number=block_number,
        )
        return com.generate_model(resp, BlockCountDown)

    def get_block_number_by_ts(
        self, timestamp: int, closest: Const = Const.BLK_NUM_CLOSEST_BEFORE
    ) -> int:
        resp = com.get_transactions(
            module=Modules.BLOCK,
            action=ApiActions.GETBLOCKNOBYTIME,
            timestamp=timestamp,
            closest=closest,
        )
        try:
            return int(resp)
        except TypeError:
            return None
