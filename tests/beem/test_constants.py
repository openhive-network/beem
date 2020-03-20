from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
import mock
import pytz
from datetime import datetime, timedelta
from parameterized import parameterized
from pprint import pprint
from beem import Hive, exceptions, constants
from beem.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.appbase = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            bundle=False,
            # Overwrite wallet to use this list of wifs only
            keys={"active": wif},
            num_retries=10
        )

    def test_constants(self):
        hv = self.appbase
        hive_conf = hv.get_config()
        if "HIVE_100_PERCENT" in hive_conf:
            HIVE_100_PERCENT = hive_conf['HIVE_100_PERCENT']
        else:
            HIVE_100_PERCENT = hive_conf['HIVEIT_100_PERCENT']
        self.assertEqual(constants.HIVE_100_PERCENT, HIVE_100_PERCENT)

        if "HIVE_1_PERCENT" in hive_conf:
            HIVE_1_PERCENT = hive_conf['HIVE_1_PERCENT']
        else:
            HIVE_1_PERCENT = hive_conf['HIVEIT_1_PERCENT']
        self.assertEqual(constants.HIVE_1_PERCENT, HIVE_1_PERCENT)

        if "HIVE_REVERSE_AUCTION_WINDOW_SECONDS" in hive_conf:
            HIVE_REVERSE_AUCTION_WINDOW_SECONDS = hive_conf['HIVE_REVERSE_AUCTION_WINDOW_SECONDS']
        elif "HIVE_REVERSE_AUCTION_WINDOW_SECONDS_HF6" in hive_conf:
            HIVE_REVERSE_AUCTION_WINDOW_SECONDS = hive_conf['HIVE_REVERSE_AUCTION_WINDOW_SECONDS_HF6']
        else:
            HIVE_REVERSE_AUCTION_WINDOW_SECONDS = hive_conf['HIVEIT_REVERSE_AUCTION_WINDOW_SECONDS']
        self.assertEqual(constants.HIVE_REVERSE_AUCTION_WINDOW_SECONDS_HF6, HIVE_REVERSE_AUCTION_WINDOW_SECONDS)

        if "HIVE_REVERSE_AUCTION_WINDOW_SECONDS_HF20" in hive_conf:
            self.assertEqual(constants.HIVE_REVERSE_AUCTION_WINDOW_SECONDS_HF20, hive_conf["HIVE_REVERSE_AUCTION_WINDOW_SECONDS_HF20"])

        if "HIVE_VOTE_DUST_THRESHOLD" in hive_conf:
            self.assertEqual(constants.HIVE_VOTE_DUST_THRESHOLD, hive_conf["HIVE_VOTE_DUST_THRESHOLD"])

        if "HIVE_VOTE_REGENERATION_SECONDS" in hive_conf:
            HIVE_VOTE_REGENERATION_SECONDS = hive_conf['HIVE_VOTE_REGENERATION_SECONDS']
            self.assertEqual(constants.HIVE_VOTE_REGENERATION_SECONDS, HIVE_VOTE_REGENERATION_SECONDS)
        elif "HIVE_VOTING_MANA_REGENERATION_SECONDS" in hive_conf:
            HIVE_VOTING_MANA_REGENERATION_SECONDS = hive_conf["HIVE_VOTING_MANA_REGENERATION_SECONDS"]
            self.assertEqual(constants.HIVE_VOTING_MANA_REGENERATION_SECONDS, HIVE_VOTING_MANA_REGENERATION_SECONDS)
        else:
            HIVE_VOTE_REGENERATION_SECONDS = hive_conf['HIVEIT_VOTE_REGENERATION_SECONDS']
            self.assertEqual(constants.HIVE_VOTE_REGENERATION_SECONDS, HIVE_VOTE_REGENERATION_SECONDS)

        if "HIVE_ROOT_POST_PARENT" in hive_conf:
            HIVE_ROOT_POST_PARENT = hive_conf['HIVE_ROOT_POST_PARENT']
        else:
            HIVE_ROOT_POST_PARENT = hive_conf['HIVEIT_ROOT_POST_PARENT']
        self.assertEqual(constants.HIVE_ROOT_POST_PARENT, HIVE_ROOT_POST_PARENT)
