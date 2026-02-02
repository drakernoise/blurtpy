import unittest
from unittest.mock import patch
from blurtgraphenebase.bip32 import BIP32Key, CURVE_ORDER

class TestBIP32Validation(unittest.TestCase):
    def test_fromEntropy_invalid_il(self):
        # We need to mock hmac.new().digest() to return a specific value
        # il is the first 32 bytes.

        # Case 1: il is 0
        zero_il = b'\x00' * 32
        mock_digest = zero_il + b'\x01' * 32

        with patch('hmac.new') as mock_hmac:
            mock_hmac.return_value.digest.return_value = mock_digest
            with self.assertRaises(ValueError) as cm:
                BIP32Key.fromEntropy(b'\x01' * 16)
            self.assertEqual(str(cm.exception), "Invalid Il generated from entropy")

        # Case 2: il is exactly CURVE_ORDER
        il_at_order = CURVE_ORDER.to_bytes(32, 'big')
        mock_digest = il_at_order + b'\x01' * 32
        with patch('hmac.new') as mock_hmac:
            mock_hmac.return_value.digest.return_value = mock_digest
            with self.assertRaises(ValueError) as cm:
                BIP32Key.fromEntropy(b'\x01' * 16)
            self.assertEqual(str(cm.exception), "Invalid Il generated from entropy")

        # Case 3: il is > CURVE_ORDER (but still 32 bytes)
        il_above_order = (CURVE_ORDER + 1).to_bytes(32, 'big')
        mock_digest = il_above_order + b'\x01' * 32
        with patch('hmac.new') as mock_hmac:
            mock_hmac.return_value.digest.return_value = mock_digest
            with self.assertRaises(ValueError) as cm:
                BIP32Key.fromEntropy(b'\x01' * 16)
            self.assertEqual(str(cm.exception), "Invalid Il generated from entropy")

    def test_CKDpriv_invalid_il(self):
        # Create a valid BIP32Key first
        entropy = b'\x01' * 32
        m = BIP32Key.fromEntropy(entropy)

        # Mock hmac to return Il >= CURVE_ORDER
        il_at_order = CURVE_ORDER.to_bytes(32, 'big')

        with patch.object(BIP32Key, 'hmac') as mock_hmac:
            mock_hmac.return_value = (il_at_order, b'\x01' * 32)
            child = m.ChildKey(1)
            self.assertIsNone(child)

    def test_CKDpub_invalid_il(self):
        # Create a valid BIP32Key first
        entropy = b'\x01' * 32
        m = BIP32Key.fromEntropy(entropy)
        m.SetPublic()

        # Mock hmac to return Il >= CURVE_ORDER
        il_at_order = CURVE_ORDER.to_bytes(32, 'big')

        with patch.object(BIP32Key, 'hmac') as mock_hmac:
            mock_hmac.return_value = (il_at_order, b'\x01' * 32)
            child = m.ChildKey(1)
            self.assertIsNone(child)

if __name__ == '__main__':
    unittest.main()
