# -*- coding: utf-8 -*-
import unittest
from blurtpy import Blurt, exceptions
from blurtpy.instance import set_shared_blurt_instance
from blurtpy.account import Account
from blurtpy.witness import Witness
from blurtpy.nodelist import NodeList
from .nodes import get_blurt_nodes, get_blurt_nodes


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bts = Blurt(
            node=get_blurt_nodes(),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_blurt_instance(cls.bts)

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
