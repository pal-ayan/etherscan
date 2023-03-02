import os

import pandas as pd
import requests
from furl import furl

from src.enums import AccountActions, AccountsTags, ApiParams, Const, Modules


class Accounts:
    def __init__(self):
        pass

    def _get_response_result(self, url: str):
        print(url)
        resp = requests.get(url)
        if resp.status_code == 200:
            if resp.json()["status"] == "1":
                return resp.json()["result"]
            else:
                raise Exception(resp.json()["message"], resp.json())
        raise Exception("Api Error")

    def _get_base_url(self) -> furl:
        f = furl(os.getenv("MAINNET_BASE_URL"))
        f /= ""
        f.args[ApiParams.APIKEY.value] = os.getenv("API_KEY")
        f.args[ApiParams.MODULE.value] = Modules.ACCOUNT.value
        return f

    def _build_param(self, f: furl, param: str = None, value=None):
        if param is None or value is None:
            return
        f.args[param] = value

    def _get_value(self, value: None):
        if value is None:
            return None
        return value.value

    def _get_transactions(
        self,
        address: str = None,
        sort_order: Const = None,
        limit: int = None,
        action: AccountActions = None,
        start_block: int = None,
        end_block: int = None,
        hash: str = None,
        contract_address: str = None,
        page: int = None,
        block_type: Const = None,
    ) -> pd.DataFrame:
        f = self._get_base_url()
        self._build_param(f, ApiParams.ACTION.value, action.value)
        self._build_param(f, ApiParams.ADDRESS.value, address)
        self._build_param(f, ApiParams.STARTBLOCK.value, start_block)
        self._build_param(f, ApiParams.ENDBLOCK.value, end_block)
        self._build_param(f, ApiParams.OFFSET.value, limit)
        self._build_param(f, ApiParams.SORT.value, self._get_value(sort_order))
        self._build_param(f, ApiParams.HASH.value, hash)
        self._build_param(f, ApiParams.CONTRACTADDR.value, contract_address)
        self._build_param(f, ApiParams.PAGE.value, page)
        self._build_param(f, ApiParams.BLOCKTYPE.value, self._get_value(block_type))

        try:
            resp = self._get_response_result(f.url)
            df = pd.json_normalize(resp)
            return df
        except Exception as e:
            print(e.args[0])
            return None

    def get_balance(self, address: str, tag: AccountsTags) -> str:
        return self.get_balances([address], tag)[address]

    def get_balances(self, address: list[str], tag: AccountsTags) -> dict[str, int]:
        f = self._get_base_url()
        f.args[ApiParams.ACTION.value] = AccountActions.BALANCEMULTI.value
        f.args[ApiParams.ADDRESS.value] = ",".join(address)
        f.args[ApiParams.TAG.value] = tag.value
        resp = self._get_response_result(f.url)
        ret = {}
        for item in resp:
            ret[item["account"]] = int(item["balance"]) / Const.WEI.value
        return ret

    def get_normal_transactions(
        self,
        address: str,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort_order: Const = Const.SORT_ASC,
        start_block: int = 0,
        end_block: int = 99999999,
        page: int = 0,
    ) -> pd.DataFrame:
        return self._get_transactions(
            address,
            sort_order,
            limit,
            AccountActions.TXLIST,
            start_block,
            end_block,
            page=page,
        )

    def get_internal_transactions_by_address(
        self,
        address: str,
        limit: int,
        sort_order: Const = Const.SORT_ASC,
        start_block: int = 0,
        end_block: int = 99999999,
    ) -> pd.DataFrame:
        return self._get_transactions(
            address,
            sort_order,
            limit,
            AccountActions.TXLISTINTERNAL,
            start_block,
            end_block,
        )

    def get_internal_transactions_by_hash(
        self,
        txhash: str,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=AccountActions.TXLISTINTERNAL,
            hash=txhash,
        )

    def get_internal_transactions_by_block_range(
        self,
        start_block: int,
        end_block: int,
        sort: Const = Const.SORT_ASC,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=AccountActions.TXLISTINTERNAL,
            start_block=start_block,
            end_block=end_block,
            sort_order=sort,
            limit=limit,
            page=page,
        )

    def get_erc20_token_transfer_events(
        self,
        address: str,
        contract_address: str,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort: Const = Const.SORT_ASC,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=AccountActions.TOKENTX,
            address=address,
            contract_address=contract_address,
            page=page,
            limit=limit,
            sort_order=sort,
        )

    def get_erc721_token_transfer_events(
        self,
        address: str,
        contract_address: str,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort: Const = Const.SORT_ASC,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=AccountActions.TOKENNFTTX,
            address=address,
            contract_address=contract_address,
            page=page,
            limit=limit,
            sort_order=sort,
        )

    def get_erc1155_token_transfer_events(
        self,
        address: str,
        contract_address: str,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort: Const = Const.SORT_ASC,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=AccountActions.TOKEN1155TX,
            address=address,
            contract_address=contract_address,
            page=page,
            limit=limit,
            sort_order=sort,
        )

    def get_blocks_mined_by_address(
        self,
        address: str,
        block_type: Const = Const.BLOCKTYPE_BLOCKS,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=AccountActions.GETMINEDBLOCKS,
            address=address,
            page=page,
            limit=limit,
            block_type=block_type,
        )
