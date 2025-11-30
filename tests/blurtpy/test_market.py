# -*- coding: utf-8 -*-
import unittest
from parameterized import parameterized
from pprint import pprint
from blurtpy import Blurt
from blurtpy.market import Market
from blurtpy.price import Price
from blurtpy.asset import Asset
from blurtpy.amount import Amount
from blurtpy.instance import set_shared_blurt_instance
from .nodes import get_blurt_nodes, get_blurt_nodes

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bts = Blurt(
            node=get_blurt_nodes(),
            nobroadcast=True,
            unsigned=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        self.assertEqual(volume['HBD']["symbol"], u'HBD')

    def test_orderbook(self):
        bts = self.bts
        m = Market(u'BLURT:VESTS', blurt_instance=bts)
        orderbook = m.orderbook(limit=10)
        self.assertEqual(len(orderbook['asks_date']), 10)
        self.assertEqual(len(orderbook['asks']), 10)
        self.assertEqual(len(orderbook['bids_date']), 10)
        self.assertEqual(len(orderbook['bids']), 10)

    def test_recenttrades(self):
        bts = self.bts
        m = Market(u'BLURT:VESTS', blurt_instance=bts)
        recenttrades = m.recent_trades(limit=10)
        recenttrades_raw = m.recent_trades(limit=10, raw_data=True)
        self.assertEqual(len(recenttrades), 10)
        self.assertEqual(len(recenttrades_raw), 10)

    def test_trades(self):
        bts = self.bts
        m = Market(u'BLURT:VESTS', blurt_instance=bts)
        trades = m.trades(limit=10)
        trades_raw = m.trades(limit=10, raw_data=True)
        trades_history = m.trade_history(limit=10)
        self.assertEqual(len(trades), 10)
        self.assertTrue(len(trades_history) > 0)
        self.assertEqual(len(trades_raw), 10)

    def test_market_history(self):
        bts = self.bts
        m = Market(u'BLURT:VESTS', blurt_instance=bts)
        buckets = m.market_history_buckets()
        history = m.market_history(buckets[2])
        self.assertTrue(len(history) > 0)

    def test_accountopenorders(self):
        bts = self.bts
        m = Market(u'BLURT:VESTS', blurt_instance=bts)
        openOrder = m.accountopenorders("test")
        self.assertTrue(isinstance(openOrder, list))

    def test_buy(self):
        bts = self.bts
        m = Market(u'BLURT:VESTS', blurt_instance=bts)
        bts.txbuffer.clear()
        tx = m.buy(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.100 HIVE', blurt_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 HBD', blurt_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE", blurt_instance=bts)
        tx = m.buy(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.100 HIVE', blurt_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 HBD', blurt_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE", blurt_instance=bts)
        a = Amount(0.1, "HIVE", blurt_instance=bts)
        tx = m.buy(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(a), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 HBD', blurt_instance=bts)), op["amount_to_sell"])

    def test_sell(self):
        bts = self.bts
        bts.txbuffer.clear()
        m = Market(u'HIVE:HBD', blurt_instance=bts)
        tx = m.sell(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.500 HBD', blurt_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 HIVE', blurt_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE")
        tx = m.sell(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 HBD', blurt_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 HIVE', blurt_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"HBD:HIVE", blurt_instance=bts)
        a = Amount(0.1, "HIVE", blurt_instance=bts)
        tx = m.sell(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 HBD', blurt_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 HIVE', blurt_instance=bts)), op["amount_to_sell"])

    def test_cancel(self):
        bts = self.bts
        bts.txbuffer.clear()
        m = Market(u'HIVE:HBD', blurt_instance=bts)
        tx = m.cancel(5, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_cancel"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "test",
            op["owner"])

    def test_blurt_usb_impied(self):
        bts = self.bts
        m = Market(u'HIVE:HBD', blurt_instance=bts)
        blurt_usd = m.blurt_usd_implied()
        self.assertGreater(blurt_usd, 0)
