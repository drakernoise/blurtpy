# -*- coding: utf-8 -*-
import unittest
from parameterized import parameterized
from blurtpy import Blurt, Blurt
from blurtpy.instance import set_shared_blockchain_instance
from blurtpy.transactionbuilder import TransactionBuilder
from blurtbase.signedtransactions import Signed_Transaction
from blurtbase.operations import Transfer
from blurtpy.account import Account
from blurtpy.block import Block
from blurtgraphenebase.base58 import Base58
from blurtpy.amount import Amount
from blurtpy.exceptions import (
    InsufficientAuthorityError,
    MissingKeyError,
    InvalidWifError
)
from blurtstorage.exceptions import WalletLocked
from blurtapi import exceptions
from blurtpy.wallet import Wallet
from blurtpy.utils import formatTimeFromNow
from .nodes import get_blurt_nodes, get_blurt_nodes
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
wif2 = "5JKu2dFfjKAcD6aP1HqBDxMNbdwtvPS99CaxBzvMYhY94Pt6RDS"
wif3 = "5K1daXjehgPZgUHz6kvm55ahEArBHfCHLy6ew8sT7sjDb76PU2P"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        node_list = get_blurt_nodes()
        cls.stm = Blurt(
            node=node_list,
            keys={"active": wif, "owner": wif2, "memo": wif3},
            nobroadcast=True,
            num_retries=10
        )
        cls.blurtit = Blurt(
            node="https://api.blurtit.com",
            nobroadcast=True,
            keys={"active": wif, "owner": wif2, "memo": wif3},
            num_retries=10
        )
        set_shared_blockchain_instance(cls.stm)
        cls.stm.set_default_account("test")

    def test_emptyTransaction(self):
        stm = self.stm
        tx = TransactionBuilder(blurt_instance=stm)
        self.assertTrue(tx.is_empty())
        self.assertTrue(tx["ref_block_num"] is not None)

    def test_verify_transaction(self):
        stm = self.stm
        block = Block(22005665, blurt_instance=stm)
        trx = block.transactions[28]
        signed_tx = Signed_Transaction(trx)
        key = signed_tx.verify(chain=stm.chain_params, recover_parameter=False)
        public_key = format(Base58(key[0]), stm.prefix)
        self.assertEqual(public_key, "STM4xA6aCu23rKxsEZWF2xVYJvJAyycuoFxBRQEuQ5Hc7UtFET7fT")
