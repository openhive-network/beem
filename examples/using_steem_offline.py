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
from beem.witness import Witness
from beembase import operations
from beem.transactionbuilder import TransactionBuilder
from beemgraphenebase.account import PasswordKey, PrivateKey, PublicKey
from beem.hive import Hive
from beem.utils import parse_time, formatTimedelta
from beemapi.exceptions import NumRetriesReached
from beem.nodelist import NodeList
from beembase.transactions import getBlockParams
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# example wif
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


if __name__ == "__main__":
    hv_online = Hive()
    ref_block_num, ref_block_prefix = getBlockParams(hv_online)
    print("ref_block_num %d - ref_block_prefix %d" % (ref_block_num, ref_block_prefix))

    hv = Hive(offline=True)

    op = operations.Transfer({'from': 'beembot',
                              'to': 'thecrazygm',
                              'amount': "0.001 HBD",
                              'memo': ""})
    tb = TransactionBuilder(hive_instance=hv)

    tb.appendOps([op])
    tb.appendWif(wif)
    tb.constructTx(ref_block_num=ref_block_num, ref_block_prefix=ref_block_prefix)
    tx = tb.sign(reconstruct_tx=False)
    print(tx.json())
