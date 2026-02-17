import unittest
import logging
from blurtgraphenebase.account import PrivateKey

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAuditKeys(unittest.TestCase):
    def test_private_key_repr_redaction(self):
        """Verify that PrivateKey.__repr__ does not leak the key"""
        logger.info("Testing PrivateKey.__repr__ redaction...")
        
        # Generate a random key
        pk = PrivateKey()
        wif = str(pk)
        
        # Get the repr
        r = repr(pk)
        
        logger.info(f"WIF: {wif}")
        logger.info(f"Repr: {r}")
        
        # Check that WIF is NOT in repr
        self.assertNotIn(wif, r, "WIF found in __repr__!")
        
        # Check that it matches the expected redacted format
        self.assertEqual(r, "<PrivateKey: ...>", "Unexpected __repr__ format")
        
        # Check that we can still get the key if we really want to (via str or bytes)
        self.assertEqual(str(pk), wif)
        self.assertTrue(len(bytes(pk)) > 0)

if __name__ == '__main__':
    unittest.main()
