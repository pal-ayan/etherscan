import pandas as pd
from furl import furl

import src.commons as com
from src.enums import AccountsTags, ApiActions, ApiParams, Const, Modules


class Accounts:
    def __init__(self):
        pass

    def _get_transactions(
        self,
        address: str = None,
        sort_order: Const = None,
        limit: int = None,
        action: ApiActions = None,
        start_block: int = None,
        end_block: int = None,
        hash: str = None,
        contract_address: str = None,
        page: int = None,
        block_type: Const = None,
    ) -> pd.DataFrame:
        return com.get_dataframe(
            com.get_transactions(
                Modules.ACCOUNT,
                address=address,
                sort_order=sort_order,
                limit=limit,
                action=action,
                start_block=start_block,
                end_block=end_block,
                hash=hash,
                contract_address=contract_address,
                page=page,
                block_type=block_type,
            )
        )

    def get_balance(self, address: str, tag: AccountsTags) -> str:
        return self.get_balances([address], tag)[address]

    def get_balances(self, address: list[str], tag: AccountsTags) -> dict[str, int]:
        f = com.get_base_url(Modules.ACCOUNT)
        f.args[ApiParams.ACTION.value] = ApiActions.BALANCEMULTI.value
        f.args[ApiParams.ADDRESS.value] = ",".join(address)
        f.args[ApiParams.TAG.value] = tag.value
        resp = com.get_response_result(f.url)
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
            ApiActions.TXLIST,
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
            ApiActions.TXLISTINTERNAL,
            start_block,
            end_block,
        )

    def get_internal_transactions_by_hash(
        self,
        txhash: str,
    ) -> pd.DataFrame:
        return self._get_transactions(
            action=ApiActions.TXLISTINTERNAL,
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
            action=ApiActions.TXLISTINTERNAL,
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
            action=ApiActions.TOKENTX,
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
            action=ApiActions.TOKENNFTTX,
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
            action=ApiActions.TOKEN1155TX,
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
            action=ApiActions.GETMINEDBLOCKS,
            address=address,
            page=page,
            limit=limit,
            block_type=block_type,
        )
