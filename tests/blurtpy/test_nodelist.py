# -*- coding: utf-8 -*-
import unittest
from blurtpy import Blurt, exceptions, Blurt
from blurtpy.instance import set_shared_blockchain_instance
from blurtpy.account import Account
from blurtpy.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        cls.bts = Blurt(
            node=nodelist.get_blurt_nodes(),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_blockchain_instance(cls.bts)

    def test_get_nodes(self):
        nodelist = NodeList()
        all_nodes = nodelist.get_nodes(exclude_limited=False, dev=True, testnet=True, testnetdev=True)
        self.assertEqual(len(nodelist) - 16, len(all_nodes))
        https_nodes = nodelist.get_nodes(wss=False)
        self.assertEqual(https_nodes[0][:5], 'https')

    def test_blurt_nodes(self):
        nodelist = NodeList()
        nodelist.update_nodes()
        blurt_nodes = nodelist.get_blurt_nodes()
        for node in blurt_nodes:
            blockchainobject = Blurt(node=node)
            assert blockchainobject.is_blurt

    def test_blurt_nodes(self):
        nodelist = NodeList()
        nodelist.update_nodes()
        blurt_nodes = nodelist.get_blurt_nodes()
        for node in blurt_nodes:
            blockchainobject = Blurt(node=node)
            assert blockchainobject.is_blurt

    def test_nodes_update(self):
        nodelist = NodeList()
        all_nodes = nodelist.get_blurt_nodes()
        nodelist.update_nodes(blockchain_instance=self.bts)
        nodes = nodelist.get_blurt_nodes()
        self.assertIn(nodes[0], all_nodes)

        all_nodes = nodelist.get_blurt_nodes()
        nodelist.update_nodes(blockchain_instance=self.bts)
        nodes = nodelist.get_blurt_nodes()
        self.assertIn(nodes[0], all_nodes)        
