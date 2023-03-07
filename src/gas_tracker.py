from __future__ import annotations

import json
from typing import List, Union

from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, Modules


class GasOracle(BaseModel):
    LastBlock: int
    SafeGasPrice: int
    ProposeGasPrice: int
    FastGasPrice: int
    suggestBaseFee: float
    gasUsedRatio: List[float]


class GasTracker:
    def get_estimated_conf_time(
        self,
        gas_price: int,
    ) -> Union[None, int]:
        resp = com.get_transactions(
            module=Modules.GASTRACKER,
            action=ApiActions.GASESTIMATE,
            gas_price=gas_price,
        )

        if resp is None:
            return None
        else:
            return int(resp)

    def get_gas_oracle(self) -> Union[None, GasOracle]:
        resp = com.get_transactions(
            module=Modules.GASTRACKER,
            action=ApiActions.GASORACLE,
        )

        if resp is None:
            return None

        result_json = json.loads(json.dumps(resp))
        ls_ratio = result_json["gasUsedRatio"].split(",")
        result_json["gasUsedRatio"] = ls_ratio
        return GasOracle.parse_obj(result_json)
