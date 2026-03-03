import unittest

from blurtbase.memo import get_shared_secret
from blurtgraphenebase.account import PrivateKey


class TestMemoSharedSecret(unittest.TestCase):
    def test_shared_secret_is_commutative_and_64_hex(self):
        alice_priv = PrivateKey()
        bob_priv = PrivateKey()

        ss1 = get_shared_secret(alice_priv, bob_priv.pubkey)
        ss2 = get_shared_secret(bob_priv, alice_priv.pubkey)

        self.assertEqual(ss1, ss2)
        self.assertEqual(len(ss1), 64)
        int(ss1, 16)  # must be valid hex


if __name__ == '__main__':
    unittest.main()
