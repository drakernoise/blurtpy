# -*- coding: utf-8 -*-
from blurtpy.nodelist import NodeList
from blurtpy import Blurt, Blurt


def get_blurt_nodes():
    nodelist = NodeList()
    nodes = nodelist.get_blurt_nodes()
    nodelist.update_nodes(blockchain_instance=Blurt(node=nodes, num_retries=10))
    return nodelist.get_blurt_nodes()
    #return "https://beta.openblurt.network"


def get_blurt_nodes():
    return "https://api.blurtit.com"


def get_blurt_nodes():
    return "https://rpc.blurt.world"
