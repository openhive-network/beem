from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from datetime import datetime, timedelta
import time
import io
import logging

from beem.blockchain import Blockchain
from beem.block import Block
from beem.account import Account
from beem.amount import Amount
from beemgraphenebase.account import PasswordKey, PrivateKey, PublicKey
from beem.hive import Hive
from beem.utils import parse_time, formatTimedelta
from beemapi.exceptions import NumRetriesReached
from beem.nodelist import NodeList
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    # stm = Hive(node="https://testnet.timcliff.com/")
    # stm = Hive(node="https://testnet.hiveitdev.com")
    stm = Hive(node="https://api.hiveit.com")
    stm.wallet.unlock(pwd="pwd123")

    account = Account("beembot", hive_instance=stm)
    print(account.get_voting_power())

    account.transfer("holger80", 0.001, "HBD", "test")
