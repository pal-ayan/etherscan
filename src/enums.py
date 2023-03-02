import enum


class ApiParams(enum.Enum):
    ACTION = "action"
    ADDRESS = "address"
    TAG = "tag"
    APIKEY = "apikey"
    MODULE = "module"
    STARTBLOCK = "startblock"
    ENDBLOCK = "endblock"
    OFFSET = "offset"
    SORT = "sort"
    HASH = "txhash"
    CONTRACTADDR = "contractaddress"
    PAGE = "page"
    BLOCKTYPE = "blocktype"


class AccountsTags(enum.Enum):
    EARLIEST = "earliest"
    PENDING = "pending"
    LATEST = "latest"


class AccountActions(enum.Enum):
    BALANCE = "balance"
    BALANCEMULTI = "balancemulti"
    TXLIST = "txlist"
    TXLISTINTERNAL = "txlistinternal"
    TOKENTX = "tokentx"
    TOKENNFTTX = "tokennfttx"
    TOKEN1155TX = "token1155tx"
    GETMINEDBLOCKS = "getminedblocks"


class Modules(enum.Enum):
    ACCOUNT = "account"


class Const(enum.Enum):
    WEI = 1000000000000000000
    SORT_ASC = "asc"
    SORT_DESC = "desc"
    BLOCKTYPE_BLOCKS = "blocks"
    BLOCKTYPE_UNCLES = "uncles"
    RESP_LENGTH_LIMIT = 10_000
