from src.accounts import Accounts
from src.enums import *


def run():
    print("Running")
    acc = Accounts()
    bal = acc.get_balance(
        address="0x4AB1BF59F3802f8CD78f9CE488D6778Eac12bAA9", tag=AccountsTags.LATEST
    )
    print(bal)


if __name__ == "__main__":
    run()
