import json
import os
import re
import zlib

import pandas as pd
import requests
from furl import furl
from pydantic import BaseModel

from src.enums import ApiActions, ApiParams, Const, Modules


def get_base_url(module: Modules) -> furl:
    f = furl(os.getenv("MAINNET_BASE_URL"))
    f /= ""
    f.args[ApiParams.APIKEY.value] = os.getenv("API_KEY")
    f.args[ApiParams.MODULE.value] = module.value
    return f


# TODO: messy code, clean this up
def get_all_pages_in_result(f):
    resp = get_response_result(f.url)
    try:
        current_page = f.query.params[ApiParams.PAGE.value]
    except KeyError:
        return resp
    if int(current_page) == 0:
        return resp
    body_count = len(resp)
    while body_count == int(f.query.params[ApiParams.OFFSET.value]):
        new_page = int(current_page) + 1
        f.args[ApiParams.PAGE.value] = new_page
        try:
            new_resp = get_response_result(f.url)
        except Exception as e:
            print(e)
            return resp
        body_count = len(new_resp)
        resp.extend(new_resp)
        current_page = new_page
    return resp


def get_response_result(url: str):
    print(url)
    resp = requests.get(url)
    if resp.status_code == 200:
        if resp.json()["status"] == "1":
            return resp.json()["result"]
        else:
            raise Exception(resp.json()["message"], resp.json()["result"], resp.json())
    raise Exception("Api Error")


def build_param(f: furl, param: str, value=None):
    if value is None or (type(value) == str and len(value) == 0):
        return
    f.args[param] = value


def get_value(value: None):
    if value is None:
        return None
    return value.value


def get_transactions(
    module: Modules,
    address: str = None,
    sort_order: Const = None,
    limit: int = None,
    action: ApiActions = None,
    start_block: int = None,
    end_block: int = None,
    hash: str = None,
    contract_address: str = None,
    contract_addresses: list = [],
    page: int = None,
    block_type: Const = None,
    block_number: int = None,
    timestamp: int = None,
    closest: Const = None,
    fromBlock: int = None,
    toBlock: int = None,
    all_pages: int = 0,
):
    f = get_base_url(module)
    build_param(f, ApiParams.ACTION.value, action.value)
    build_param(f, ApiParams.ADDRESS.value, address)
    build_param(f, ApiParams.STARTBLOCK.value, start_block)
    build_param(f, ApiParams.ENDBLOCK.value, end_block)
    build_param(f, ApiParams.OFFSET.value, limit)
    build_param(f, ApiParams.SORT.value, get_value(sort_order))
    build_param(f, ApiParams.HASH.value, hash)
    build_param(f, ApiParams.CONTRACTADDR.value, contract_address)
    build_param(f, ApiParams.CONTRACTADDRS.value, ",".join(contract_addresses))
    build_param(f, ApiParams.PAGE.value, page)
    build_param(f, ApiParams.BLOCKTYPE.value, get_value(block_type))
    build_param(f, ApiParams.BLOCKNO.value, block_number)
    build_param(f, ApiParams.TIMESTAMP.value, timestamp)
    build_param(f, ApiParams.CLOSEST.value, get_value(closest))
    build_param(f, ApiParams.FROMBLOCK.value, fromBlock)
    build_param(f, ApiParams.TOBLOCK.value, toBlock)

    if all_pages == 0 and page == 0 and limit < Const.RESP_LENGTH_LIMIT.value:
        raise Exception(
            "if 'limit' is other than default, please update the 'page' to a minimum of 1"
        )

    if all_pages == 1 and page == 0:
        build_param(f, ApiParams.PAGE.value, 1)

    try:
        if all_pages == 1:
            return get_all_pages_in_result(f)
        else:
            return get_response_result(f.url)
    except Exception as e:
        print(e)
        # print(e.args[0], e.args[1])
        return None


def get_dataframe(json: json = None) -> pd.DataFrame:
    if json is None:
        return None
    return pd.json_normalize(json)


def compress(str: str) -> bytes:
    return zlib.compress(str.encode())


def decompress(bytes: bytes) -> str:
    return zlib.decompress(bytes).decode()


def generate_model(
    result_object,
    model: BaseModel,
) -> BaseModel:
    if result_object == None:
        return None
    else:
        result_object = json.loads(json.dumps(result_object))
        return model.parse_obj(result_object)
