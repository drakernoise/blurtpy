# -*- coding: utf-8 -*-
import unittest
from parameterized import parameterized
from pprint import pprint
from blurtpy import Blurt
from blurtpy.witness import Witness, Witnesses, WitnessesVotedByAccount, WitnessesRankedByVote
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
        cls.blurtit = Blurt(
            node=get_blurt_nodes(),
            nobroadcast=True,
            unsigned=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_blurt_instance(cls.bts)
        cls.bts.set_default_account("test")

    @parameterized.expand([
        ("normal"),
        ("blurtit"),
    ])
    def test_feed_publish(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.blurtit
        bts.txbuffer.clear()
        w = Witness("gtg", blurt_instance=bts)
        tx = w.feed_publish("4 %s" % bts.backed_token_symbol, "1 %s" % bts.token_symbol)
        self.assertEqual(
            (tx["operations"][0][0]),
            "feed_publish"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "gtg",
            op["publisher"])

    @parameterized.expand([
        ("normal"),
        ("blurtit"),
    ])
    def test_update(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.blurtit
        bts.txbuffer.clear()
        w = Witness("gtg", blurt_instance=bts)
        props = {"account_creation_fee": "0.1 %s" % bts.token_symbol,
                 "maximum_block_size": 32000,
                 "sbd_interest_rate": 0}
        tx = w.update(wif, "", props)
        self.assertEqual((tx["operations"][0][0]), "witness_update")
        op = tx["operations"][0][1]
        self.assertIn(
            "gtg",
            op["owner"])

    @parameterized.expand([
        ("normal"),
        ("blurtit"),
    ])
    def test_witnesses(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.blurtit
        w = Witnesses(blurt_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("normal"),
    ])
    def test_WitnessesVotedByAccount(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.blurtit
        w = WitnessesVotedByAccount("gtg", blurt_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("normal"),
        ("blurtit"),
    ])
    def test_WitnessesRankedByVote(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.blurtit
        w = WitnessesRankedByVote(blurt_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("normal"),
        ("blurtit"),
    ])
    def test_export(self, node_param):
        if node_param == "normal":
            bts = self.bts
        else:
            bts = self.blurtit
        owner = "gtg"
        if bts.rpc.get_use_appbase():
            witness = bts.rpc.find_witnesses({'owners': [owner]}, api="database")['witnesses']
            if len(witness) > 0:
                witness = witness[0]
        else:
            witness = bts.rpc.get_witness_by_account(owner)

        w = Witness(owner, blurt_instance=bts)
        keys = list(witness.keys())
        json_witness = w.json()
        exclude_list = ['votes', 'virtual_last_update', 'virtual_scheduled_time', 'last_aslot',
                        'last_confirmed_block_num', 'available_witness_account_subsidies']
        for k in keys:
            if k not in exclude_list:
                if isinstance(witness[k], dict) and isinstance(json_witness[k], list):
                    self.assertEqual(list(witness[k].values()), json_witness[k])
                else:
                    self.assertEqual(witness[k], json_witness[k])
