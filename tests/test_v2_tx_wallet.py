import unittest

from blurtgraphenebase.account import PrivateKey
from blurtpyv2.tx import TxBuilder
from blurtpyv2.wallet import KeyStore


class TestV2TxBuilder(unittest.TestCase):
    def test_build_without_rpc(self):
        builder = TxBuilder(rpc=None)
        builder.add_operation([0, {"foo": "bar"}])
        tx = builder.build()

        self.assertIn("expiration", tx)
        self.assertIn("operations", tx)
        self.assertEqual(len(tx["operations"]), 1)
        # ref_block_* may be None without RPC
        self.assertTrue("ref_block_num" in tx)
        self.assertTrue("ref_block_prefix" in tx)


class TestV2KeyStore(unittest.TestCase):
    def test_add_and_sign(self):
        keystore = KeyStore()
        priv = PrivateKey()
        pub = keystore.add_private_key(priv)

        message = b"keystore sign test"
        signature = keystore.sign(message, pub)
        self.assertTrue(len(signature) > 0)

        fetched = keystore.get_private_key(pub)
        self.assertIsNotNone(fetched)

    def test_remove_key(self):
        keystore = KeyStore()
        priv = PrivateKey()
        pub = keystore.add_private_key(priv)
        keystore.remove_public_key(pub)
        self.assertIsNone(keystore.get_private_key(pub))


if __name__ == "__main__":
    unittest.main()
