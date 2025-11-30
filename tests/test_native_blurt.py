import unittest
import logging
from blurtpy import Blurt
from blurtpy.account import Account
from blurtpy.amount import Amount
from blurtpy.exceptions import AccountDoesNotExistsException, MissingKeyError
from blurtstorage.exceptions import WalletLocked
from blurtgraphenebase.account import PasswordKey

# Configure logging to capture details during stress testing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User provided key for 'draktest'
ACTIVE_KEY = "5K8sEXDvidZijhKpYDyWxyKSP22T3UdU8276YEsmcDgwbmgRS6K"
ACCOUNT_NAME = "draktest"

class TestNativeBlurt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a robust node list to test failover capabilities
        cls.nodes = [
            "https://rpc.blurt.world",
            "https://rpc.beblurt.com",
            "https://blurt-rpc.saboin.com",
            "https://rpc.blurt.one"
        ]
        # Initialize Blurt with the active key
        cls.blurt = Blurt(node=cls.nodes, keys=[ACTIVE_KEY], num_retries=3)
        logger.info(f"Initialized Blurt with nodes: {cls.nodes}")

    def test_01_connection_and_props(self):
        """
        STRESS TEST: Fetch dynamic global properties multiple times.
        This ensures the library can maintain a stable connection and handle potential node flakiness.
        """
        logger.info("Testing connection stability...")
        for i in range(5):
            props = self.blurt.get_dynamic_global_properties()
            self.assertIsNotNone(props)
            self.assertIn('head_block_number', props)
            logger.info(f"Iteration {i+1}: Head Block {props['head_block_number']}")

    def test_02_account_fetch_integrity(self):
        """
        DATA INTEGRITY: Fetch account data and verify types and values.
        """
        logger.info(f"Fetching account {ACCOUNT_NAME}...")
        account = Account(ACCOUNT_NAME, blockchain_instance=self.blurt)
        self.assertEqual(account.name, ACCOUNT_NAME)
        
        # Verify balance types
        balance = account.get_balance('available', 'BLURT')
        self.assertIsInstance(balance, Amount)
        self.assertEqual(balance.symbol, "BLURT")
        logger.info(f"Account Balance: {balance}")

    def test_03_account_not_found(self):
        """
        ERROR HANDLING: Ensure proper exception for non-existent account.
        """
        fake_account = "account_that_should_not_exist_9999"
        logger.info(f"Testing non-existent account: {fake_account}")
        with self.assertRaises(AccountDoesNotExistsException):
            Account(fake_account, blockchain_instance=self.blurt)

    def test_04_transaction_signing(self):
        """
        SECURITY & CRYPTO: Create and sign a transaction without broadcasting.
        This verifies the Active Key is valid and the signing mechanism works.
        """
        logger.info("Testing transaction signing (dry-run)...")
        account = Account(ACCOUNT_NAME, blockchain_instance=self.blurt)
        
        # Create a dummy transfer of 0.001 BLURT to self (safe for testing)
        # 'nobroadcast=True' ensures we don't actually spend money, just test the crypto
        tx = self.blurt.transfer(
            ACCOUNT_NAME, 0.001, "BLURT", memo="Native Test Signing", account=ACCOUNT_NAME, nobroadcast=True
        )
        
        # Verify it's signed
        self.assertIsNotNone(tx.get('signatures'))
        self.assertGreater(len(tx['signatures']), 0)
        logger.info("Transaction signed successfully!")

    def test_05_missing_key_protection(self):
        """
        SECURITY: Ensure operations fail safely when the key is missing.
        """
        logger.info("Testing missing key protection...")
        # Instance without keys
        b_no_key = Blurt(node=self.nodes)
        
        with self.assertRaises((MissingKeyError, WalletLocked)):
            b_no_key.transfer(ACCOUNT_NAME, 0.001, "BLURT", account=ACCOUNT_NAME, nobroadcast=True)

    def test_06_history_resilience(self):
        """
        PERFORMANCE: Fetch a chunk of history to test API response handling.
        """
        logger.info("Testing history retrieval...")
        account = Account(ACCOUNT_NAME, blockchain_instance=self.blurt)
        # Fetch last 50 ops
        history = []
        for op in account.history(batch_size=50):
            history.append(op)
            if len(history) >= 50:
                break
        self.assertTrue(len(history) > 0)
        logger.info(f"Retrieved {len(history)} history items.")

if __name__ == '__main__':
    unittest.main()
