# -*- coding: utf-8 -*-
import unittest
from blurtpy import Blurt
from blurtpy.conveyor import Conveyor
from blurtpy.instance import set_shared_blurt_instance
from .nodes import get_blurt_nodes, get_blurt_nodes

wif = '5Jh1Gtu2j4Yi16TfhoDmg8Qj3ULcgRi7A49JXdfUUTVPkaFaRKz'


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        stm = Blurt(node=get_blurt_nodes(), nobroadcast=True,
                    num_retries=10, expiration=120)
        set_shared_blurt_instance(stm)

    def test_healthcheck(self):
        health = Conveyor().healthcheck()
        self.assertTrue('version' in health)
        self.assertTrue('ok' in health)
        self.assertTrue('date' in health)

if __name__ == "__main__":
    unittest.main()
