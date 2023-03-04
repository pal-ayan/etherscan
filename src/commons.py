import json
import os
import re

import pandas as pd
import requests
from furl import furl

from src.enums import ApiActions, ApiParams, Const, Modules


def get_base_url(module: Modules) -> furl:
    f = furl(os.getenv("MAINNET_BASE_URL"))
    f /= ""
    f.args[ApiParams.APIKEY.value] = os.getenv("API_KEY")
    f.args[ApiParams.MODULE.value] = module.value
    return f


def get_response_result(url: str):
    print(url)
    resp = requests.get(url)
    if resp.status_code == 200:
        if resp.json()["status"] == "1":
            return resp.json()["result"]
        else:
            raise Exception(resp.json()["message"], resp.json())
    raise Exception("Api Error")


def build_param(f: furl, param: str = None, value=None):
    if param is None or value is None:
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
    page: int = None,
    block_type: Const = None,
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
    build_param(f, ApiParams.PAGE.value, page)
    build_param(f, ApiParams.BLOCKTYPE.value, get_value(block_type))

    try:
        return get_response_result(f.url)
    except Exception as e:
        print(e.args[0])
        return None


def get_dataframe(json: json = None) -> pd.DataFrame:
    if json is None:
        return None
    return pd.json_normalize(json)


def multireplace(string, replacements, ignore_case=False):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param bool ignore_case: whether the match should be case insensitive
    :rtype: str
    """
    if not replacements:
        # Edge case that'd produce a funny regex and cause a KeyError
        return string

    # If case insensitive, we need to normalize the old string so that later a replacement
    # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
    # "HEY", "hEy", etc.
    if ignore_case:

        def normalize_old(s):
            return s.lower()

        re_mode = re.IGNORECASE

    else:

        def normalize_old(s):
            return s

        re_mode = 0

    replacements = {normalize_old(key): val for key, val in replacements.items()}

    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)

    # Create a big OR regex that matches any of the substrings to replace
    pattern = re.compile("|".join(rep_escaped), re_mode)

    # For each match, look up the new string in the replacements, being the key the normalized old string
    return pattern.sub(
        lambda match: replacements[normalize_old(match.group(0))], string
    )
