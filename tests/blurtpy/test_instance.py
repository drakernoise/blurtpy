# -*- coding: utf-8 -*-
import string
import unittest
import random
from parameterized import parameterized
from pprint import pprint
from blurtpy import Blurt, Blurt
from blurtpy.amount import Amount
from blurtpy.witness import Witness
from blurtpy.account import Account
from blurtpy.instance import set_shared_blurt_instance, shared_blurt_instance, set_shared_config
from blurtpy.blockchain import Blockchain
from blurtpy.block import Block
from blurtpy.market import Market
from blurtpy.price import Price
from blurtpy.comment import Comment
from blurtpy.vote import Vote
from blurtapi.exceptions import RPCConnection
from blurtpy.wallet import Wallet
from blurtpy.transactionbuilder import TransactionBuilder
from blurtbase.operations import Transfer
from blurtgraphenebase.account import PasswordKey, PrivateKey, PublicKey
from blurtpy.utils import parse_time, formatTimedelta
from .nodes import get_blurt_nodes, get_blurt_nodes

# Py3 compatibility
import sys

core_unit = "STM"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stm = Blurt(node=get_blurt_nodes())
        stm.config.refreshBackup()
        stm.set_default_nodes(["xyz"])
        del stm

        cls.urls = get_blurt_nodes()
        cls.bts = Blurt(
            node=cls.urls,
            nobroadcast=True,
            num_retries=10
        )
        set_shared_blurt_instance(cls.bts)
        acc = Account("fullnodeupdate", blurt_instance=cls.bts)
        comment = Comment(acc.get_blog_entries(limit=5)[1], blurt_instance=cls.bts)
        cls.authorperm = comment.authorperm
        votes = comment.get_votes(raw_data=True)
        last_vote = votes[-1]
        cls.authorpermvoter = comment['authorperm'] + '|' + last_vote["voter"]

    @classmethod
    def tearDownClass(cls):
        stm = Blurt(node=get_blurt_nodes())
        stm.config.recover_with_latest_backup()

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_account(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            acc = Account("test")
            self.assertIn(acc.blockchain.rpc.url, self.urls)
            self.assertIn(acc["balance"].blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test", blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            acc = Account("test", blurt_instance=stm)
            self.assertIn(acc.blockchain.rpc.url, self.urls)
            self.assertIn(acc["balance"].blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test")

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_amount(self, node_param):
        if node_param == "instance":
            stm = Blurt(node="https://abc.d", autoconnect=False, num_retries=1)
            set_shared_blurt_instance(self.bts)
            o = Amount("1 %s" % self.bts.backed_token_symbol)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 %s" % self.bts.backed_token_symbol, blurt_instance=stm)
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Amount("1 %s" % self.bts.backed_token_symbol, blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 %s" % self.bts.backed_token_symbol)

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_block(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Block(1)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1, blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Block(1, blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1)

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_blockchain(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Blockchain()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain(blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Blockchain(blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain()

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_comment(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Comment(self.authorperm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm, blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Comment(self.authorperm, blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm)

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_market(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Market()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market(blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Market(blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market()

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_price(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol))
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol), blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol), blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol))

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_vote(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Vote(self.authorpermvoter)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter, blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Vote(self.authorpermvoter, blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter)

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_wallet(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Wallet()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet(blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
                o.blockchain.get_config()
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Wallet(blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet()
                o.blockchain.get_config()

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_witness(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Witness("gtg")
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg", blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Witness("gtg", blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg")

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_transactionbuilder(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = TransactionBuilder()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder(blurt_instance=Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
                o.blockchain.get_config()
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = TransactionBuilder(blurt_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder()
                o.blockchain.get_config()

    @parameterized.expand([
        ("instance"),
        ("blurt")
    ])
    def test_blurt(self, node_param):
        if node_param == "instance":
            set_shared_blurt_instance(self.bts)
            o = Blurt(node=self.urls)
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = Blurt(node="https://abc.d", autoconnect=False, num_retries=1)
                stm.get_config()
        else:
            set_shared_blurt_instance(Blurt(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = stm
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = shared_blurt_instance()
                stm.get_config()

    def test_config(self):
        set_shared_config({"node": self.urls})
        set_shared_blurt_instance(None)
        o = shared_blurt_instance()
        self.assertIn(o.rpc.url, self.urls)
