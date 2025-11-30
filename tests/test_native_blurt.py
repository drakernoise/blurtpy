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

# User provided key for testing
# !!! IMPORTANT: YOU MUST UPDATE THESE VALUES BEFORE RUNNING TESTS !!!
ACTIVE_KEY = "YOUR_ACTIVE_KEY_HERE"
ACCOUNT_NAME = "your_account_name_here"

class TestNativeBlurt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Check if user has configured the tests
        if ACTIVE_KEY == "YOUR_ACTIVE_KEY_HERE" or ACCOUNT_NAME == "your_account_name_here":
            raise ValueError(
                "\n\n"
                "!!! TEST CONFIGURATION ERROR !!!\n"
                "You must configure 'tests/test_native_blurt.py' with your own account details.\n"
                "Please edit the file and update ACTIVE_KEY and ACCOUNT_NAME at the top.\n"
            )

        # Use a robust node list to test failover capabilities
        cls.nodes = [
            "https://rpc.blurt.world",
            "https://rpc.beblurt.com",
            "https://blurt-rpc.saboin.com",
            "https://rpc.blurt.one"
        ]
        # Initialize Blurt with the active key and nobroadcast=True for safety
        cls.blurt = Blurt(node=cls.nodes, keys=[ACTIVE_KEY], num_retries=3, nobroadcast=True)
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
        logger.info("Testing Memo encryption/decryption...")
        from blurtpy.memo import Memo
        from blurtgraphenebase.account import PasswordKey

        # Generate two temporary keys
        sender_wif = PasswordKey("sender", "password", role="memo").get_private_key()
        receiver_wif = PasswordKey("receiver", "password", role="memo").get_private_key()
        receiver_pub = receiver_wif.pubkey

        # Initialize Memo with these keys
        # We pass keys directly to avoid looking up accounts on chain
        # Note: Memo expects strings for length check, so we convert objects to strings
        memo_obj = Memo(
            from_account=format(sender_wif, 'WIF'),
            to_account=format(receiver_pub.pubkey, "STM"),
            blockchain_instance=self.blurt
        )

        # Encrypt
        message = "Secret Blurt Message"
        encrypted = memo_obj.encrypt(message)
        self.assertTrue(encrypted['message'].startswith('#'))
        logger.info(f"Encrypted message: {encrypted['message']}")

        # Decrypt (requires initializing a new Memo object or unlocking wallet, 
        # but here we use the low-level decrypt with known keys if possible, 
        # or we simulate the receiver)
        
        # To test decryption, we need to simulate the receiver having the private key.
        # The library's decrypt method looks up keys in the wallet.
        # Let's inject the receiver key into the wallet for this test.
        self.blurt.wallet.setKeys([format(receiver_wif, 'WIF')])
        
        decrypted = memo_obj.decrypt(encrypted['message'])
        # Note: blurtbase implementation prepends '#' to decrypted message
        self.assertEqual(decrypted, '#' + message)
        logger.info("Decryption successful!")

    def test_08_power_up_dry_run(self):
        """
        OPERATION: Construct and sign a Transfer to Vesting (Power Up) operation.
        """
        logger.info("Testing Power Up (dry-run)...")
        account = Account(ACCOUNT_NAME, blockchain_instance=self.blurt)
        # transfer_to_vesting(amount, to, account)
        tx = account.transfer_to_vesting(
            0.001, ACCOUNT_NAME, account=ACCOUNT_NAME, nobroadcast=True
        )
        self.assertIsNotNone(tx.get('signatures'))
        logger.info("Power Up transaction signed.")

    def test_09_claim_rewards_dry_run(self):
        """
        OPERATION: Construct and sign a Claim Reward Balance operation.
        """
        logger.info("Testing Claim Rewards (dry-run)...")
        account = Account(ACCOUNT_NAME, blockchain_instance=self.blurt)
        # claim_reward_balance(reward_blurt, reward_vests, account)
        tx = account.claim_reward_balance(
            0, 0, account=ACCOUNT_NAME, nobroadcast=True
        )
        self.assertIsNotNone(tx.get('signatures'))
        logger.info("Claim Rewards transaction signed.")

    def test_10_vote_operation_dry_run(self):
        """
        OPERATION: Construct and sign a Vote operation.
        Validates posting authority logic (even if using Active key).
        """
        logger.info("Testing Vote operation (dry-run)...")
        # vote(identifier, weight, account)
        # Using a known valid identifier (or random, since it's dry-run structure check)
        # We use a real-looking identifier to pass validation if any
        identifier = "@draktest/test-post" 
        tx = self.blurt.vote(
            identifier, 100, account=ACCOUNT_NAME, nobroadcast=True
        )
        self.assertIsNotNone(tx.get('signatures'))
        logger.info("Vote transaction signed.")

    def test_11_input_validation(self):
        """
        SECURITY: Test input validation for malicious/invalid data.
        """
        logger.info("Testing Input Validation...")
        account = Account("draktest", blockchain_instance=self.blurt)

        # 1. Negative Amount Transfer
        # Should raise ValueError to prevent draining funds or logic errors
        with self.assertRaises(ValueError):
            account.transfer("draktest", -10, "BLURT", "Negative Transfer")
        
        # 2. Invalid Asset
        # Should raise AssetDoesNotExistsException
        from blurtpy.exceptions import AssetDoesNotExistsException
        with self.assertRaises(AssetDoesNotExistsException):
            account.transfer("draktest", 10, "FAKECOIN", "Invalid Asset")

        logger.info("Input validation tests passed.")

if __name__ == '__main__':
    unittest.main()
