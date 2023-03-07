from typing import Union

import src.commons as com
from src.enums import AccountsTags, ApiActions, Modules


class Tokens:
    def get_erc_20_total_token_supply(
        self,
        contract_address: str,
    ) -> Union[int, None]:
        resp = com.get_transactions(
            module=Modules.STATS,
            action=ApiActions.TOKENSUPPLY,
            contract_address=contract_address,
        )

        if resp is None:
            return None
        else:
            return int(resp)

    def get_erc_20_toke_acc_bal(
        self, contract_address: str, address: str
    ) -> Union[int, None]:
        resp = com.get_transactions(
            module=Modules.ACCOUNT,
            action=ApiActions.TOKENBALANCE,
            address=address,
            contract_address=contract_address,
            tag=AccountsTags.LATEST,
        )

        if resp is None:
            return None
        else:
            return int(resp)
