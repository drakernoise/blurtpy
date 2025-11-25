# -*- coding: utf-8 -*-
import string
import unittest
from parameterized import parameterized
import random
import json
from pprint import pprint
from blurtpy import Blurt
from blurtpy.amount import Amount
from blurtpy.memo import Memo
from blurtpy.version import version as blurtpy_version
from blurtpy.wallet import Wallet
from blurtpy.witness import Witness
from blurtpy.account import Account
from blurtgraphenebase.account import PrivateKey
from blurtpy.instance import set_shared_blurt_instance, shared_blurt_instance
from .nodes import get_blurt_nodes, get_blurt_nodes
# Py3 compatibility
import sys
core_unit = "STM"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stm = shared_blurt_instance()
        stm.config.refreshBackup()

        cls.stm = Blurt(
            node=get_blurt_nodes(),
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            num_retries=10
            # Overwrite wallet to use this list of wifs only
        )

        cls.stm.set_default_account("test")
        set_shared_blurt_instance(cls.stm)
        # self.stm.newWallet("TestingOneTwoThree")

        cls.wallet = Wallet(blurt_instance=cls.stm)
        cls.wallet.wipe(True)
        cls.wallet.newWallet("TestingOneTwoThree")
        cls.wallet.unlock(pwd="TestingOneTwoThree")
        cls.wallet.addPrivateKey(wif)

    @classmethod
    def tearDownClass(cls):
        stm = shared_blurt_instance()
        stm.config.recover_with_latest_backup()

    def test_set_default_account(self):
        stm = self.stm
        stm.set_default_account("blurtpybot")

        self.assertEqual(stm.config["default_account"], "blurtpybot")
