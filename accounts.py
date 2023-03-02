import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv
from furl import furl

from enums import AccountActions, AccountsTags, ApiParams, Const, Modules


class Accounts:
    def __init__(self):
        pass

    def _get_json(self, url: str) -> str:
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

        try:
            resp = self._get_json(f.url)
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
        resp = self._get_json(f.url)
        ret = {}
        for item in resp:
            ret[item["account"]] = int(item["balance"]) / Const.WEI.value
        return ret

    def get_normal_transactions(
        self,
        address: str,
        sort_order: Const,
        limit: int,
        start_block: int = 0,
        end_block: int = 99999999,
    ) -> pd.DataFrame:
        return self._get_transactions(
            address, sort_order, limit, AccountActions.TXLIST, start_block, end_block
        )

    def get_internal_transactions_by_address(
        self,
        address: str,
        sort_order: Const,
        limit: int,
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
        sort: Const,
        page: int = 1,
        limit: int = 10000,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=AccountActions.TXLISTINTERNAL,
            start_block=start_block,
            end_block=end_block,
            sort_order=sort,
            limit=limit,
            page=page,
        )


if __name__ == "__main__":
    load_dotenv()
    acc = Accounts()
    """
    bal = acc.get_balance(
        "0x4AB1BF59F3802f8CD78f9CE488D6778Eac12bAA9",
        AccountsTags.LATEST,
    )
    print(bal)

    df = acc.get_normal_transactions(
        "0x4AB1BF59F3802f8CD78f9CE488D6778Eac12bAA9", Const.SORT_ASC, 10000
    )

    print(df.head(8))
    
    df = acc.get_internal_transactions_by_address(
        "0x4AB1BF59F3802f8CD78f9CE4886778Eac12bAA9", Const.SORT_ASC, 10000
    )

    print(df.head(8))
    
    df = acc.get_internal_transactions_by_hash(
        "0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170"
    )

    print(df.head(8))
    """
    df = acc.get_internal_transactions_by_block_range(
        14409823, 14409824, Const.SORT_ASC
    )

    print(df.info())
