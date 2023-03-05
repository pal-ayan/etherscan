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
    CONTRACTADDRS = "contractaddresses"
    PAGE = "page"
    BLOCKTYPE = "blocktype"
    BLOCKNO = "blockno"
    CLOSEST = "closest"
    TIMESTAMP = "timestamp"
    FROMBLOCK = "fromBlock"
    TOBLOCK = "toBlock"


class AccountsTags(enum.Enum):
    EARLIEST = "earliest"
    PENDING = "pending"
    LATEST = "latest"


class ApiActions(enum.Enum):
    BALANCE = "balance"
    BALANCEMULTI = "balancemulti"
    TXLIST = "txlist"
    TXLISTINTERNAL = "txlistinternal"
    TOKENTX = "tokentx"
    TOKENNFTTX = "tokennfttx"
    TOKEN1155TX = "token1155tx"
    GETMINEDBLOCKS = "getminedblocks"
    GETABI = "getabi"
    GETSOURCECODE = "getsourcecode"
    GETCONTRACTCREATION = "getcontractcreation"
    GETSTATUS = "getstatus"
    GETTXRECEIPTSTATUS = "gettxreceiptstatus"
    GETBLOCKREWARD = "getblockreward"
    GETBLOCKCOUNTDOWN = "getblockcountdown"
    GETBLOCKNOBYTIME = "getblocknobytime"
    GETLOGS = "getLogs"


class Modules(enum.Enum):
    ACCOUNT = "account"
    CONTRACT = "contract"
    TRANSACTION = "transaction"
    BLOCK = "block"
    LOGS = "logs"


class Const(enum.Enum):
    WEI = 1000000000000000000
    SORT_ASC = "asc"
    SORT_DESC = "desc"
    BLOCKTYPE_BLOCKS = "blocks"
    BLOCKTYPE_UNCLES = "uncles"
    RESP_LENGTH_LIMIT = 10_000
    RESP_LENGTH_LIMIT_LOGS = 1_000
    BLK_NUM_CLOSEST_BEFORE = "before"
    BLK_NUM_CLOSEST_AFTER = "after"
