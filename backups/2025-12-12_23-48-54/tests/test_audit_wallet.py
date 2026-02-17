import unittest
import os
import logging
from blurtpy import Blurt
from blurtpy.wallet import Wallet
from blurtstorage import InRamEncryptedKeyStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAuditWallet(unittest.TestCase):
    def setUp(self):
        # Use InRamEncryptedKeyStore to avoid touching disk
        self.blurt = Blurt(node=["https://rpc.beblurt.com"])
        # Mock the wallet to use RAM store
        self.blurt.wallet.store = InRamEncryptedKeyStore(config=self.blurt.config)
        
    def test_wallet_encryption(self):
        """Verify that keys are encrypted in the store"""
        logger.info("Testing wallet encryption...")
        
        password = "supersecretpassword"
        wif = "5J7yas9WhDbvJoBUtdLAEREf4YbX7bDiZDCcBHbqerYjpfetmX8"
        
        # Create wallet
        self.blurt.wallet.create(password)
        self.assertFalse(self.blurt.wallet.locked())
        
        # Add key
        self.blurt.wallet.addPrivateKey(wif)
        
        # Check internal store content
        # The store should contain the encrypted key, not the WIF
        pub = self.blurt.wallet.publickey_from_wif(wif)
        encrypted_wif = self.blurt.wallet.store.get(pub)
        
        logger.info(f"Stored WIF (Encrypted): {encrypted_wif}")
        
        self.assertNotEqual(encrypted_wif, wif, "Key stored in plaintext!")
        self.assertTrue(encrypted_wif.startswith("6P"), "Not a BIP38 encrypted key (should start with 6P)")
        
        # Lock wallet
        self.blurt.wallet.lock()
        self.assertTrue(self.blurt.wallet.locked())
        
        # Try to access key without unlock
        with self.assertRaises(Exception):
            self.blurt.wallet.getPrivateKeyForPublicKey(pub)
            
        # Unlock and access
        self.blurt.wallet.unlock(password)
        decrypted_wif = self.blurt.wallet.getPrivateKeyForPublicKey(pub)
        self.assertEqual(str(decrypted_wif), wif)

if __name__ == '__main__':
    unittest.main()
