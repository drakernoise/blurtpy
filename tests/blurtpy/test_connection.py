# -*- coding: utf-8 -*-
import unittest
from blurtpy import Blurt, Blurt
from blurtpy.account import Account
from blurtpy.instance import set_shared_blurt_instance, SharedInstance
from blurtpy.blockchainobject import BlockchainObject
from blurtpy.nodelist import NodeList

import logging
log = logging.getLogger()


class Testcases(unittest.TestCase):

    def test_stm1stm2(self):
        nodelist = NodeList()
        nodelist.update_nodes(blurt_instance=Blurt(node=nodelist.get_blurt_nodes(), num_retries=10))
        b1 = Blurt(
            node="https://api.blurtit.com",
            nobroadcast=True,
            num_retries=10
        )
        node_list = nodelist.get_blurt_nodes()

        b2 = Blurt(
            node=node_list,
            nobroadcast=True,
            num_retries=10
        )

        self.assertNotEqual(b1.rpc.url, b2.rpc.url)

    def test_default_connection(self):
        nodelist = NodeList()
        nodelist.update_nodes(blurt_instance=Blurt(node=nodelist.get_blurt_nodes(), num_retries=10))

        b2 = Blurt(
            node=nodelist.get_blurt_nodes(),
            nobroadcast=True,
        )
        set_shared_blurt_instance(b2)
        bts = Account("blurtpy")
        self.assertEqual(bts.blockchain.prefix, "STM")
