# -*- coding: utf-8 -*-
import unittest
import pytz
from datetime import datetime, timedelta
from parameterized import parameterized
from pprint import pprint
from blurtpy import Blurt, exceptions, constants
from .nodes import get_blurt_nodes, get_blurt_nodes

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.appbase = Blurt(
            node=get_blurt_nodes(),
            nobroadcast=True,
            bundle=False,
            # Overwrite wallet to use this list of wifs only
            keys={"active": wif},
            num_retries=10
        )

    def test_constants(self):
        stm = self.appbase
        blurt_conf = stm.get_config()
        if "BLURT_100_PERCENT" in blurt_conf:
            BLURT_100_PERCENT = blurt_conf['BLURT_100_PERCENT']
        else:
            BLURT_100_PERCENT = blurt_conf['STEEMIT_100_PERCENT']
        self.assertEqual(constants.BLURT_100_PERCENT, BLURT_100_PERCENT)

        if "BLURT_1_PERCENT" in blurt_conf:
            BLURT_1_PERCENT = blurt_conf['BLURT_1_PERCENT']
        else:
            BLURT_1_PERCENT = blurt_conf['STEEMIT_1_PERCENT']
        self.assertEqual(constants.BLURT_1_PERCENT, BLURT_1_PERCENT)

        if "STEEM_REVERSE_AUCTION_WINDOW_SECONDS" in blurt_conf:
            STEEM_REVERSE_AUCTION_WINDOW_SECONDS = blurt_conf['STEEM_REVERSE_AUCTION_WINDOW_SECONDS']
        elif "BLURT_REVERSE_AUCTION_WINDOW_SECONDS_HF6" in blurt_conf:
            STEEM_REVERSE_AUCTION_WINDOW_SECONDS = blurt_conf['BLURT_REVERSE_AUCTION_WINDOW_SECONDS_HF6']
        else:
            STEEM_REVERSE_AUCTION_WINDOW_SECONDS = blurt_conf['STEEMIT_REVERSE_AUCTION_WINDOW_SECONDS']
        self.assertEqual(constants.BLURT_REVERSE_AUCTION_WINDOW_SECONDS_HF6, STEEM_REVERSE_AUCTION_WINDOW_SECONDS)

        if "BLURT_REVERSE_AUCTION_WINDOW_SECONDS_HF20" in blurt_conf:
            self.assertEqual(constants.BLURT_REVERSE_AUCTION_WINDOW_SECONDS_HF20, blurt_conf["BLURT_REVERSE_AUCTION_WINDOW_SECONDS_HF20"])

        if "BLURT_VOTE_DUST_THRESHOLD" in blurt_conf:
            self.assertEqual(constants.BLURT_VOTE_DUST_THRESHOLD, blurt_conf["BLURT_VOTE_DUST_THRESHOLD"])

        if "BLURT_VOTE_REGENERATION_SECONDS" in blurt_conf:
            BLURT_VOTE_REGENERATION_SECONDS = blurt_conf['BLURT_VOTE_REGENERATION_SECONDS']
            self.assertEqual(constants.BLURT_VOTE_REGENERATION_SECONDS, BLURT_VOTE_REGENERATION_SECONDS)
        elif "BLURT_VOTING_MANA_REGENERATION_SECONDS" in blurt_conf:
            BLURT_VOTING_MANA_REGENERATION_SECONDS = blurt_conf["BLURT_VOTING_MANA_REGENERATION_SECONDS"]
            self.assertEqual(constants.BLURT_VOTING_MANA_REGENERATION_SECONDS, BLURT_VOTING_MANA_REGENERATION_SECONDS)
        else:
            BLURT_VOTE_REGENERATION_SECONDS = blurt_conf['STEEMIT_VOTE_REGENERATION_SECONDS']
            self.assertEqual(constants.BLURT_VOTE_REGENERATION_SECONDS, BLURT_VOTE_REGENERATION_SECONDS)

        if "BLURT_ROOT_POST_PARENT" in blurt_conf:
            BLURT_ROOT_POST_PARENT = blurt_conf['BLURT_ROOT_POST_PARENT']
        else:
            BLURT_ROOT_POST_PARENT = blurt_conf['STEEMIT_ROOT_POST_PARENT']
        self.assertEqual(constants.BLURT_ROOT_POST_PARENT, BLURT_ROOT_POST_PARENT)