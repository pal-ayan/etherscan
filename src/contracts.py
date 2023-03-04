import json

import pandas as pd
from furl import furl

import src.commons as com
from src.enums import ApiActions, ApiParams, Modules


class Contracts:
    def _get_base_url(self) -> furl:
        f = com.get_base_url()
        f.args[ApiParams.MODULE.value] = Modules.ACCOUNT.value
        return f

    def get_abi_for_verified_contract_src_code(
        self,
        address: str,
    ) -> pd.DataFrame:
        resp = com.get_transactions(
            module=Modules.CONTRACT, address=address, action=ApiActions.GETABI
        )

        if resp is None:
            return None
        else:
            resp = resp.replace("\\", "")
            resp = json.loads(resp)
            return com.get_dataframe(resp)
