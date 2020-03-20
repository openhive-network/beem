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

password = "secretPassword"
username = "beem5"
useWallet = False
walletpassword = "123"

if __name__ == "__main__":
    testnet_node = "https://testnet.hive.vc"
    hv = Hive(node=testnet_node)
    prefix = hv.prefix
    # curl --data "username=username&password=secretPassword" https://testnet.hive.vc/create
    if useWallet:
        hv.wallet.wipe(True)
        hv.wallet.create(walletpassword)
        hv.wallet.unlock(walletpassword)
    active_key = PasswordKey(username, password, role="active", prefix=prefix)
    owner_key = PasswordKey(username, password, role="owner", prefix=prefix)
    posting_key = PasswordKey(username, password, role="posting", prefix=prefix)
    memo_key = PasswordKey(username, password, role="memo", prefix=prefix)
    active_pubkey = active_key.get_public_key()
    owner_pubkey = owner_key.get_public_key()
    posting_pubkey = posting_key.get_public_key()
    memo_pubkey = memo_key.get_public_key()
    active_privkey = active_key.get_private_key()
    posting_privkey = posting_key.get_private_key()
    owner_privkey = owner_key.get_private_key()
    memo_privkey = memo_key.get_private_key()
    if useWallet:
        hv.wallet.addPrivateKey(owner_privkey)
        hv.wallet.addPrivateKey(active_privkey)
        hv.wallet.addPrivateKey(memo_privkey)
        hv.wallet.addPrivateKey(posting_privkey)
    else:
        hv = Hive(node=testnet_node,
                    wif={'active': str(active_privkey),
                         'posting': str(posting_privkey),
                         'memo': str(memo_privkey)})
    account = Account(username, hive_instance=hv)
    if account["name"] == "beem":
        account.disallow("beem1", permission='posting')
        account.allow('beem1', weight=1, permission='posting', account=None)
        account.follow("beem1")
    elif account["name"] == "beem5":
        account.allow('beem4', weight=2, permission='active', account=None)
    if useWallet:
        hv.wallet.getAccountFromPrivateKey(str(active_privkey))

    # hv.create_account("beem1", creator=account, password=password1)

    account1 = Account("beem1", hive_instance=hv)
    b = Blockchain(hive_instance=hv)
    blocknum = b.get_current_block().identifier

    account.transfer("beem1", 1, "HBD", "test")
    b1 = Block(blocknum, hive_instance=hv)
