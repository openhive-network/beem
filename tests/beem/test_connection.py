import unittest
from beem import Hive
from beem.account import Account
from beem.instance import set_shared_hive_instance, SharedInstance
from beem.blockchainobject import BlockchainObject
from beem.nodelist import NodeList

import logging
log = logging.getLogger()


class Testcases(unittest.TestCase):

    def test_hv1hv2(self):
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        b1 = Hive(
            node="https://api.hive.blog",
            nobroadcast=True,
            num_retries=10
        )
        node_list = nodelist.get_nodes(exclude_limited=True)

        b2 = Hive(
            node=node_list,
            nobroadcast=True,
            num_retries=10
        )

        self.assertNotEqual(b1.rpc.url, b2.rpc.url)

    def test_default_connection(self):
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))

        b2 = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
        )
        set_shared_hive_instance(b2)
        bts = Account("beem")
        self.assertEqual(bts.hive.prefix, "STM")
