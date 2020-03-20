from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from beem import Hive, exceptions
from beem.instance import set_shared_hive_instance
from beem.account import Account
from beem.witness import Witness
from beem.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_hive_instance(cls.bts)

    def test_Account(self):
        with self.assertRaises(
            exceptions.AccountDoesNotExistsException
        ):
            Account("FOObarNonExisting")

        c = Account("test")
        self.assertEqual(c["name"], "test")
        self.assertIsInstance(c, Account)

    def test_Witness(self):
        with self.assertRaises(
            exceptions.WitnessDoesNotExistsException
        ):
            Witness("FOObarNonExisting")

        c = Witness("jesta")
        self.assertEqual(c["owner"], "jesta")
        self.assertIsInstance(c.account, Account)
