# -*- coding: utf-8 -*-
from blurtpy import Blurt
from blurtpy.instance import set_shared_blurt_instance
from blurtpy.amount import Amount
from blurtpy.price import Price, Order, FilledOrder
from blurtpy.asset import Asset
import unittest
from .nodes import get_blurt_nodes, get_blurt_nodes


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        blurt = Blurt(
            node=get_blurt_nodes(),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_blurt_instance(blurt)

    def test_init(self):
        # self.assertEqual(1, 1)

        Price("0.315 BLURT/VESTS")
        Price(1.0, "BLURT/VESTS")
        Price(0.315, base="BLURT", quote="VESTS")
        Price(0.315, base=Asset("BLURT"), quote=Asset("VESTS"))
        Price({
            "base": {"amount": 1, "asset_id": "BLURT"},
            "quote": {"amount": 10, "asset_id": "VESTS"}})
        Price("", quote="10 VESTS", base="1 BLURT")
        Price("10 VESTS", "1 BLURT")
        Price(Amount("10 VESTS"), Amount("1 BLURT"))

    def test_multiplication(self):
        p1 = Price(10.0, "BLURT/VESTS")
        p2 = Price(5.0, "VESTS/BLURT")
        p3 = p1 * p2
        p4 = p3.as_base("HBD")
        p4_2 = p3.as_quote("VESTS")

        self.assertEqual(p4["quote"]["symbol"], "VESTS")
        self.assertEqual(p4["base"]["symbol"], "HBD")
        # 10 BLURT/VESTS * 0.2 VESTS/BLURT = 50 VESTS/VESTS = 0.02 VESTS/VESTS
        self.assertEqual(float(p4), 0.02)
        self.assertEqual(p4_2["quote"]["symbol"], "VESTS")
        self.assertEqual(p4_2["base"]["symbol"], "HBD")
        self.assertEqual(float(p4_2), 0.02)
        p3 = p1 * 5
        self.assertEqual(float(p3), 50)

        # Inline multiplication
        p5 = Price(10.0, "BLURT/VESTS")
        p5 *= p2
        p4 = p5.as_base("HBD")
        self.assertEqual(p4["quote"]["symbol"], "VESTS")
        self.assertEqual(p4["base"]["symbol"], "HBD")
        # 10 BLURT/VESTS * 0.2 VESTS/BLURT = 2 VESTS/VESTS = 0.02 VESTS/VESTS
        self.assertEqual(float(p4), 0.02)
        p6 = Price(10.0, "BLURT/VESTS")
        p6 *= 5
        self.assertEqual(float(p6), 50)

    def test_div(self):
        p1 = Price(10.0, "BLURT/VESTS")
        p2 = Price(5.0, "BLURT/VESTS")

        # 10 BLURT/VESTS / 5 BLURT/VESTS = 2 VESTS/VESTS
        p3 = p1 / p2
        p4 = p3.as_base("VESTS")
        self.assertEqual(p4["base"]["symbol"], "VESTS")
        self.assertEqual(p4["quote"]["symbol"], "HBD")
        # 10 BLURT/VESTS * 0.2 VESTS/BLURT = 2 VESTS/VESTS = 0.5 VESTS/VESTS
        self.assertEqual(float(p4), 2)

    def test_div2(self):
        p1 = Price(10.0, "BLURT/VESTS")
        p2 = Price(5.0, "BLURT/VESTS")

        # 10 BLURT/VESTS / 5 BLURT/VESTS = 2 VESTS/VESTS
        p3 = p1 / p2
        self.assertTrue(isinstance(p3, (float, int)))
        self.assertEqual(float(p3), 2.0)
        p3 = p1 / 5
        self.assertEqual(float(p3), 2.0)
        p3 = p1 / Amount("1 HBD")
        self.assertEqual(float(p3), 0.1)
        p3 = p1
        p3 /= p2
        self.assertEqual(float(p3), 2.0)
        p3 = p1
        p3 /= 5
        self.assertEqual(float(p3), 2.0)

    def test_ltge(self):
        p1 = Price(10.0, "BLURT/VESTS")
        p2 = Price(5.0, "BLURT/VESTS")

        self.assertTrue(p1 > p2)
        self.assertTrue(p2 < p1)
        self.assertTrue(p1 > 5)
        self.assertTrue(p2 < 10)

    def test_leeq(self):
        p1 = Price(10.0, "BLURT/VESTS")
        p2 = Price(5.0, "BLURT/VESTS")

        self.assertTrue(p1 >= p2)
        self.assertTrue(p2 <= p1)
        self.assertTrue(p1 >= 5)
        self.assertTrue(p2 <= 10)

    def test_ne(self):
        p1 = Price(10.0, "BLURT/VESTS")
        p2 = Price(5.0, "BLURT/VESTS")

        self.assertTrue(p1 != p2)
        self.assertTrue(p1 == p1)
        self.assertTrue(p1 != 5)
        self.assertTrue(p1 == 10)

    def test_order(self):
        order = Order(Amount("2 VESTS"), Amount("1 BLURT"))
        self.assertTrue(repr(order) is not None)

    def test_filled_order(self):
        order = {"date": "1900-01-01T00:00:00", "current_pays": "2 VESTS", "open_pays": "1 BLURT"}
        filledOrder = FilledOrder(order)
        self.assertTrue(repr(filledOrder) is not None)
        self.assertEqual(filledOrder.json()["current_pays"], Amount("2.000 HBD").json())
