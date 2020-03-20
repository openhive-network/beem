from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
import random
from parameterized import parameterized
from pprint import pprint
from beem import Hive
from beem.amount import Amount
from beem.witness import Witness
from beem.account import Account
from beem.instance import set_shared_hive_instance, shared_hive_instance, set_shared_config
from beem.blockchain import Blockchain
from beem.block import Block
from beem.market import Market
from beem.price import Price
from beem.comment import Comment
from beem.vote import Vote
from beemapi.exceptions import RPCConnection
from beem.wallet import Wallet
from beem.transactionbuilder import TransactionBuilder
from beembase.operations import Transfer
from beemgraphenebase.account import PasswordKey, PrivateKey, PublicKey
from beem.utils import parse_time, formatTimedelta
from beem.nodelist import NodeList

# Py3 compatibility
import sys

core_unit = "STM"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodelist = NodeList()
        cls.nodelist.update_nodes(hive_instance=Hive(node=cls.nodelist.get_nodes(exclude_limited=False), num_retries=10))
        hv = Hive(node=cls.nodelist.get_nodes())
        hv.config.refreshBackup()
        hv.set_default_nodes(["xyz"])
        del hv

        cls.urls = cls.nodelist.get_nodes(exclude_limited=True)
        cls.bts = Hive(
            node=cls.urls,
            nobroadcast=True,
            num_retries=10
        )
        set_shared_hive_instance(cls.bts)
        acc = Account("holger80", hive_instance=cls.bts)
        comment = acc.get_blog(limit=20)[-1]
        cls.authorperm = comment.authorperm
        votes = acc.get_account_votes()
        last_vote = votes[-1]
        cls.authorpermvoter = '@' + last_vote['authorperm'] + '|' + acc["name"]

    @classmethod
    def tearDownClass(cls):
        hv = Hive(node=cls.nodelist.get_nodes())
        hv.config.recover_with_latest_backup()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_account(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            acc = Account("test")
            self.assertIn(acc.hive.rpc.url, self.urls)
            self.assertIn(acc["balance"].hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test", hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            acc = Account("test", hive_instance=hv)
            self.assertIn(acc.hive.rpc.url, self.urls)
            self.assertIn(acc["balance"].hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_amount(self, node_param):
        if node_param == "instance":
            hv = Hive(node="https://abc.d", autoconnect=False, num_retries=1)
            set_shared_hive_instance(self.bts)
            o = Amount("1 HBD")
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 HBD", hive_instance=hv)
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Amount("1 HBD", hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 HBD")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_block(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Block(1)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1, hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Block(1, hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1)

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_blockchain(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Blockchain()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain(hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Blockchain(hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_comment(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Comment(self.authorperm)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm, hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Comment(self.authorperm, hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm)

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_market(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Market()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market(hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Market(hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_price(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Price(10.0, "HIVE/HBD")
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "HIVE/HBD", hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Price(10.0, "HIVE/HBD", hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "HIVE/HBD")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_vote(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Vote(self.authorpermvoter)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter, hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Vote(self.authorpermvoter, hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter)

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_wallet(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Wallet()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet(hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
                o.hive.get_config()
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Wallet(hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet()
                o.hive.get_config()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_witness(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Witness("gtg")
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg", hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Witness("gtg", hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_transactionbuilder(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = TransactionBuilder()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder(hive_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
                o.hive.get_config()
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = TransactionBuilder(hive_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder()
                o.hive.get_config()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_hive(self, node_param):
        if node_param == "instance":
            set_shared_hive_instance(self.bts)
            o = Hive(node=self.urls)
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                hv = Hive(node="https://abc.d", autoconnect=False, num_retries=1)
                hv.get_config()
        else:
            set_shared_hive_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = hv
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                hv = shared_hive_instance()
                hv.get_config()

    def test_config(self):
        set_shared_config({"node": self.urls})
        set_shared_hive_instance(None)
        o = shared_hive_instance()
        self.assertIn(o.rpc.url, self.urls)
