from __future__ import annotations

import json
from typing import List, Optional, Union

from furl import furl
from pydantic import BaseModel

import src.commons as com
from src.enums import ApiActions, ApiParams, Modules


class Input(BaseModel):
    name: str
    type: str
    indexed: Optional[bool] = None


class Output(BaseModel):
    name: str
    type: str


class AbiItem(BaseModel):
    constant: Optional[bool] = None
    inputs: List[Input]
    name: Optional[str] = None
    outputs: Optional[List[Output]] = None
    type: str
    anonymous: Optional[bool] = None


class ABI(BaseModel):
    __root__: List[AbiItem]


class ContractItem(BaseModel):
    ABI: ABI
    ContractName: str
    CompilerVersion: str
    OptimizationUsed: int
    Runs: int
    ConstructorArguments: str
    EVMVersion: str
    Library: str
    LicenseType: str
    Proxy: int
    Implementation: str
    SwarmSource: str


class CreatorItem(BaseModel):
    contractAddress: str
    contractCreator: str
    txHash: str


class Creator(BaseModel):
    __root__: List[CreatorItem]


class Contracts:
    def _get_base_url(self) -> furl:
        f = com.get_base_url(Modules.CONTRACT)
        f.args[ApiParams.MODULE.value] = Modules.ACCOUNT.value
        return f

    def get_abi_for_verified_contract_src_code(
        self,
        address: str,
    ) -> Union[None, ABI]:
        resp = com.get_transactions(
            module=Modules.CONTRACT, address=address, action=ApiActions.GETABI
        )

        if resp is None:
            return None
        else:
            resp = resp.replace("\\", "")
            resp = json.loads(resp)
            model = ABI.parse_obj(resp)
            return model

    def get_src_code_for_vc_src_code(
        self,
        address: str,
    ) -> Union[tuple[None, None], tuple[ContractItem, bytes]]:
        resp = com.get_transactions(
            module=Modules.CONTRACT,
            address=address,
            action=ApiActions.GETSOURCECODE,
        )
        if resp is None:
            return None, None
        else:
            d = resp[0]
            compressed_src_code = com.compress(d["SourceCode"])
            del d["SourceCode"]
            d["ABI"] = ABI.parse_obj(json.loads(d["ABI"]))
            return ContractItem.parse_obj(d), compressed_src_code

    def get_creator_data(
        self,
        contract_addresses: list,
    ) -> Union[None, Creator]:
        resp = com.get_transactions(
            contract_addresses=contract_addresses,
            module=Modules.CONTRACT,
            action=ApiActions.GETCONTRACTCREATION,
        )
        if resp is None:
            return None
        else:
            resp = json.loads(json.dumps(resp))
            return Creator.parse_obj(resp)
