import unittest
import logging
import time
from blurtpy import Blurt
from blurtpy.account import Account
from blurtpy.nodelist import NodeList

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestNativeBlurt(unittest.TestCase):
    def setUp(self):
        # Use known nodes directly to avoid circular dependency in NodeList update
        self.nodes = ["https://rpc.beblurt.com", "https://blurt-rpc.saboin.com", "https://rpc.blurt.world"]
        logger.info(f"Using nodes: {self.nodes}")
        
        self.blurt = Blurt(node=self.nodes)

    def test_01_connection_stability(self):
        """
        Test connection stability by making multiple requests.
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
        Test fetching a known account to verify data integrity.
        """
        logger.info("Testing account fetch integrity...")
        account_name = 'blurt' # Foundation account usually exists
        try:
            account = Account(account_name, blockchain_instance=self.blurt)
            logger.info(f"Fetched account: {account.name}")
            self.assertEqual(account.name, account_name)
            self.assertTrue('balance' in account)
        except Exception as e:
            logger.error(f"Failed to fetch account: {e}")
            raise

if __name__ == '__main__':
    unittest.main()
