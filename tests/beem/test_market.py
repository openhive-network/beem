from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from beem import Hive
from beem.market import Market
from beem.price import Price
from beem.asset import Asset
from beem.amount import Amount
from beem.instance import set_shared_hive_instance
from beem.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            unsigned=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_hive_instance(cls.bts)
        cls.bts.set_default_account("test")

    def test_market(self):
        bts = self.bts
        m1 = Market(u'HIVE', u'HBD', hive_instance=bts)
        self.assertEqual(m1.get_string(), u'HBD:HIVE')
        m2 = Market(hive_instance=bts)
        self.assertEqual(m2.get_string(), u'HBD:HIVE')
        m3 = Market(u'HIVE:HBD', hive_instance=bts)
        self.assertEqual(m3.get_string(), u'HIVE:HBD')
        self.assertTrue(m1 == m2)

        base = Asset("HBD", hive_instance=bts)
        quote = Asset("HIVE", hive_instance=bts)
        m = Market(base, quote, hive_instance=bts)
        self.assertEqual(m.get_string(), u'HIVE:HBD')

    def test_ticker(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        ticker = m.ticker()
        self.assertEqual(len(ticker), 6)
        self.assertEqual(ticker['hive_volume']["symbol"], u'HIVE')
        self.assertEqual(ticker['hbd_volume']["symbol"], u'HBD')

    def test_volume(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        volume = m.volume24h()
        self.assertEqual(volume['HIVE']["symbol"], u'HIVE')
        self.assertEqual(volume['HBD']["symbol"], u'HBD')

    def test_orderbook(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        orderbook = m.orderbook(limit=10)
        self.assertEqual(len(orderbook['asks_date']), 10)
        self.assertEqual(len(orderbook['asks']), 10)
        self.assertEqual(len(orderbook['bids_date']), 10)
        self.assertEqual(len(orderbook['bids']), 10)

    def test_recenttrades(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        recenttrades = m.recent_trades(limit=10)
        recenttrades_raw = m.recent_trades(limit=10, raw_data=True)
        self.assertEqual(len(recenttrades), 10)
        self.assertEqual(len(recenttrades_raw), 10)

    def test_trades(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        trades = m.trades(limit=10)
        trades_raw = m.trades(limit=10, raw_data=True)
        trades_history = m.trade_history(limit=10)
        self.assertEqual(len(trades), 10)
        self.assertTrue(len(trades_history) > 0)
        self.assertEqual(len(trades_raw), 10)

    def test_market_history(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        buckets = m.market_history_buckets()
        history = m.market_history(buckets[2])
        self.assertTrue(len(history) > 0)

    def test_accountopenorders(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        openOrder = m.accountopenorders("test")
        self.assertTrue(isinstance(openOrder, list))

    def test_buy(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        bts.txbuffer.clear()
        tx = m.buy(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.100 HIVE', hive_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 HBD', hive_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE", hive_instance=bts)
        tx = m.buy(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.100 HIVE', hive_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 HBD', hive_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE", hive_instance=bts)
        a = Amount(0.1, "HIVE", hive_instance=bts)
        tx = m.buy(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(a), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 HBD', hive_instance=bts)), op["amount_to_sell"])

    def test_sell(self):
        bts = self.bts
        bts.txbuffer.clear()
        m = Market(u'HIVE:HBD', hive_instance=bts)
        tx = m.sell(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.500 HBD', hive_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 HIVE', hive_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE")
        tx = m.sell(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 HBD', hive_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 HIVE', hive_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE", hive_instance=bts)
        a = Amount(0.1, "HIVE", hive_instance=bts)
        tx = m.sell(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 HBD', hive_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 HIVE', hive_instance=bts)), op["amount_to_sell"])

    def test_cancel(self):
        bts = self.bts
        bts.txbuffer.clear()
        m = Market(u'HIVE:HBD', hive_instance=bts)
        tx = m.cancel(5, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_cancel"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "test",
            op["owner"])

    def test_hive_usb_impied(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', hive_instance=bts)
        hive_usd = m.hive_usd_implied()
        self.assertGreater(hive_usd, 0)
