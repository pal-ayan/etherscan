from typing import List

from pydantic import BaseModel, Field

import src.commons as com
from src.enums import AccountsTags, ApiActions, ApiParams, Const, Modules


class BlockMinedItem(BaseModel):
    blockNumber: int
    timeStamp: int
    blockReward: int


class BlockMined(BaseModel):
    __root__: List[BlockMinedItem]


class ERC1155Item(BaseModel):
    blockNumber: int
    timeStamp: int
    hash: str
    nonce: int
    blockHash: str
    transactionIndex: int
    gas: int
    gasPrice: int
    gasUsed: int
    cumulativeGasUsed: str
    input: str
    contractAddress: str
    from_: str = Field(..., alias="from")
    to: str
    tokenID: int
    tokenValue: int
    tokenName: str
    tokenSymbol: str
    confirmations: int


class ERC1155(BaseModel):
    __root__: List[ERC1155Item]


class ERC721Item(BaseModel):
    blockNumber: int
    timeStamp: int
    hash: str
    nonce: int
    blockHash: str
    from_: str = Field(..., alias="from")
    contractAddress: str
    to: str
    tokenID: int
    tokenName: str
    tokenSymbol: str
    tokenDecimal: int
    transactionIndex: int
    gas: int
    gasPrice: int
    gasUsed: int
    cumulativeGasUsed: int
    input: str
    confirmations: int


class ERC721(BaseModel):
    __root__: List[ERC721Item]


class ERC20Item(BaseModel):
    blockNumber: int
    timeStamp: int
    hash: str
    nonce: int
    blockHash: str
    from_: str = Field(..., alias="from")
    contractAddress: str
    to: str
    value: int
    tokenName: str
    tokenSymbol: str
    tokenDecimal: int
    transactionIndex: int
    gas: int
    gasPrice: int
    gasUsed: int
    cumulativeGasUsed: int
    input: str
    confirmations: int


class ERC20(BaseModel):
    __root__: List[ERC20Item]


class InternalTxnHashItem(BaseModel):
    blockNumber: int
    timeStamp: int
    from_: str = Field(..., alias="from")
    to: str
    value: int
    contractAddress: str
    input: str
    type: str
    gas: int
    gasUsed: int
    isError: int
    errCode: str


class InternalTxnHash(BaseModel):
    __root__: List[InternalTxnHashItem]


class InternalTxnAddrItem(BaseModel):
    blockNumber: int
    timeStamp: int
    hash: str
    from_: str = Field(..., alias="from")
    to: str
    value: int
    contractAddress: str
    input: str
    type: str
    gas: int
    gasUsed: int
    traceId: int
    isError: int
    errCode: str


class InternalTxnAddr(BaseModel):
    __root__: List[InternalTxnAddrItem]


class NormalTransactionItem(BaseModel):
    blockNumber: int
    timeStamp: int
    hash: str
    nonce: int
    blockHash: str
    transactionIndex: int
    from_: str = Field(..., alias="from")
    to: str
    value: int
    gas: int
    gasPrice: int
    isError: int
    txreceipt_status: int
    input: str
    contractAddress: str
    cumulativeGasUsed: int
    gasUsed: int
    confirmations: int
    methodId: str
    functionName: str


class NormalTransaction(BaseModel):
    __root__: List[NormalTransactionItem]


class Accounts:
    def _get_result(
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
    ):
        return com.get_transactions(
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

    def get_balance(self, address: str, tag: AccountsTags) -> str:
        return self.get_balances([address], tag)[address]

    def get_balances(
        self, address: list[str], tag: AccountsTags
    ) -> dict[str, int]:
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
    ) -> NormalTransaction:
        return com.generate_model(
            result_object=self._get_result(
                address=address,
                sort_order=sort_order,
                limit=limit,
                action=ApiActions.TXLIST,
                start_block=start_block,
                end_block=end_block,
                page=page,
            ),
            model=NormalTransaction,
        )

    def get_internal_transactions_by_address(
        self,
        address: str,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort_order: Const = Const.SORT_ASC,
        start_block: int = 0,
        end_block: int = 99999999,
    ) -> InternalTxnAddr:
        return com.generate_model(
            result_object=self._get_result(
                address=address,
                sort_order=sort_order,
                limit=limit,
                action=ApiActions.TXLISTINTERNAL,
                start_block=start_block,
                end_block=end_block,
            ),
            model=InternalTxnAddr,
        )

    def get_internal_transactions_by_hash(
        self,
        txhash: str,
    ) -> InternalTxnHash:
        return com.generate_model(
            result_object=self._get_result(
                hash=txhash,
                action=ApiActions.TXLISTINTERNAL,
            ),
            model=InternalTxnHash,
        )

    def get_internal_transactions_by_block_range(
        self,
        start_block: int,
        end_block: int,
        sort: Const = Const.SORT_ASC,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
    ) -> InternalTxnHash:
        return com.generate_model(
            result_object=self._get_result(
                limit=limit,
                action=ApiActions.TXLISTINTERNAL,
                start_block=start_block,
                end_block=end_block,
                sort_order=sort,
                page=page,
            ),
            model=InternalTxnHash,
        )

    def get_erc20_token_transfer_events(
        self,
        address: str,
        contract_address: str,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort: Const = Const.SORT_ASC,
    ) -> ERC20:
        return com.generate_model(
            result_object=self._get_result(
                action=ApiActions.TOKENTX,
                address=address,
                contract_address=contract_address,
                page=page,
                limit=limit,
                sort_order=sort,
            ),
            model=ERC20,
        )

    def get_erc721_token_transfer_events(
        self,
        address: str,
        contract_address: str,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort: Const = Const.SORT_ASC,
    ) -> ERC721:
        return com.generate_model(
            result_object=self._get_result(
                action=ApiActions.TOKENNFTTX,
                address=address,
                contract_address=contract_address,
                page=page,
                limit=limit,
                sort_order=sort,
            ),
            model=ERC721,
        )

    def get_erc1155_token_transfer_events(
        self,
        address: str,
        contract_address: str,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
        sort: Const = Const.SORT_ASC,
    ) -> ERC1155:
        return com.generate_model(
            result_object=self._get_result(
                action=ApiActions.TOKEN1155TX,
                address=address,
                contract_address=contract_address,
                page=page,
                limit=limit,
                sort_order=sort,
            ),
            model=ERC1155,
        )

    def get_blocks_mined_by_address(
        self,
        address: str,
        block_type: Const = Const.BLOCKTYPE_BLOCKS,
        page: int = 0,
        limit: int = Const.RESP_LENGTH_LIMIT.value,
    ) -> BlockMined:
        return com.generate_model(
            result_object=self._get_result(
                action=ApiActions.GETMINEDBLOCKS,
                address=address,
                page=page,
                limit=limit,
                block_type=block_type,
            ),
            model=BlockMined,
        )
