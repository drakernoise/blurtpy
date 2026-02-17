import unittest

from blurtgraphenebase.account import PrivateKey, PublicKey
from blurtpyv2.crypto import EcdsaKeyAdapter, EcdsaSigner, EcdsaVerifier


class TestV2EcdsaBackend(unittest.TestCase):
    def setUp(self):
        self.wif = "5J7yas9WhDbvJoBUtdLAEREf4YbX7bDiZDCcBHbqerYjpfetmX8"
        self.message = b"v2 ecdsa test"

    def test_sign_and_verify(self):
        signer = EcdsaSigner(self.wif)
        verifier = EcdsaVerifier()
        pubkey = PublicKey(PrivateKey(self.wif).pubkey)

        signature = signer.sign(self.message)
        self.assertTrue(len(signature) > 0)
        self.assertTrue(verifier.verify(self.message, signature, pubkey))

    def test_key_adapter(self):
        adapter = EcdsaKeyAdapter()
        priv = adapter.parse_private(self.wif)
        self.assertIsInstance(priv, PrivateKey)

        pub = adapter.to_public(priv)
        self.assertIsInstance(pub, PublicKey)

        parsed_pub = adapter.parse_public(pub)
        self.assertIsInstance(parsed_pub, PublicKey)


if __name__ == "__main__":
    unittest.main()
