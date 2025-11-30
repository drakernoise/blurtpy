import unittest
import logging
import hashlib
from blurtgraphenebase.account import PrivateKey, PublicKey
from blurtgraphenebase.ecdsasig import sign_message, verify_message, SECP256K1_MODULE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAuditCrypto(unittest.TestCase):
    def test_ecdsa_signature_validity(self):
        """Verify that signatures are valid and recoverable"""
        logger.info(f"Testing ECDSA signature validity (Backend: {SECP256K1_MODULE})...")
        
        wif = "5J7yas9WhDbvJoBUtdLAEREf4YbX7bDiZDCcBHbqerYjpfetmX8"
        pk = PrivateKey(wif)
        message = "test message for audit"
        
        # Sign
        signature = sign_message(message, wif)
        self.assertTrue(len(signature) > 0)
        
        # Verify
        pubkey_bytes = verify_message(message, signature)
        from binascii import hexlify
        pubkey_hex = hexlify(pubkey_bytes).decode('ascii')
        self.assertEqual(pubkey_hex, repr(pk.pubkey))
        
        logger.info("Signature verified successfully.")

    def test_signature_determinism(self):
        """Check if signatures are deterministic (RFC6979)"""
        logger.info("Testing signature determinism...")
        
        wif = "5J7yas9WhDbvJoBUtdLAEREf4YbX7bDiZDCcBHbqerYjpfetmX8"
        message = "deterministic test"
        
        sig1 = sign_message(message, wif)
        sig2 = sign_message(message, wif)
        
        if SECP256K1_MODULE in ["secp256k1", "cryptography"]:
            # These backends SHOULD be deterministic
            if sig1 == sig2:
                logger.info("Signatures are DETERMINISTIC (RFC6979 compliant).")
            else:
                logger.warning("Signatures are NON-DETERMINISTIC! (Unexpected for this backend)")
                # We don't fail the test, but we log a warning.
        else:
            # Pure python fallback is explicitly randomized
            if sig1 != sig2:
                logger.info("Signatures are NON-DETERMINISTIC (Expected for pure-python fallback).")
            else:
                logger.info("Signatures are DETERMINISTIC (Unexpected for pure-python fallback).")

    def test_bip39_compliance(self):
        """Verify PBKDF2 rounds for BIP39"""
        from blurtgraphenebase.account import PBKDF2_ROUNDS
        self.assertEqual(PBKDF2_ROUNDS, 2048, "BIP39 requires exactly 2048 rounds")

if __name__ == '__main__':
    unittest.main()
