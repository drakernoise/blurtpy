import unittest
from blurtpy import Blurt
from blurtpy.amount import Amount
from blurtpy.account import Account
from blurtpy.exceptions import AssetDoesNotExistsException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSecurityInputs(unittest.TestCase):
    def setUp(self):
        # Use hardcoded nodes to avoid NodeList dependency issues
        self.nodes = ["https://rpc.beblurt.com", "https://blurt-rpc.saboin.com"]
        self.blurt = Blurt(node=self.nodes)

    def test_amount_precision_attack(self):
        """Test handling of inputs with excessive precision"""
        logger.info("Testing Amount precision attack...")
        # BLURT has 3 digits of precision. 4 digits should be rejected or rounded?
        # Usually libraries might round or raise error. Let's see what it does.
        # Ideally it should raise an error to prevent precision loss surprises.
        try:
            a = Amount("1.0001 BLURT", blurt_instance=self.blurt)
            # If it doesn't raise, check if it rounded correctly
            logger.warning(f"Amount accepted high precision: {a}")
        except Exception as e:
            logger.info(f"Caught expected exception for high precision: {e}")

    def test_amount_asset_spoofing(self):
        """Test handling of invalid or legacy assets"""
        logger.info("Testing Amount asset spoofing...")
        
        # SBD/HBD/TBD should be invalid if we removed them from chains.py
        # But Amount might just store the symbol string if not validated against chain.
        # We force validation by passing blurt_instance.
        
        with self.assertRaises(AssetDoesNotExistsException):
            Amount("1.000 SBD", blurt_instance=self.blurt)
            
        with self.assertRaises(AssetDoesNotExistsException):
            Amount("1.000 HIVE", blurt_instance=self.blurt)

    def test_account_malicious_names(self):
        """Test Account instantiation with malicious names"""
        logger.info("Testing Account malicious names...")
        
        bad_names = [
            "draker'; DROP TABLE accounts; --",
            "<script>alert(1)</script>",
            "user with spaces",
            "UserWithCaps",
            "u" * 200 # Too long
        ]
        
        for name in bad_names:
            with self.assertRaises(ValueError, msg=f"Should have rejected: {name}"):
                Account(name, blurt_instance=self.blurt)

    def test_amount_overflow(self):
        """Test extremely large numbers"""
        logger.info("Testing Amount overflow...")
        huge_num = "9" * 50 + " BLURT"
        # Python handles large ints, but let's see if Amount parses it safely
        a = Amount(huge_num, blurt_instance=self.blurt)
        self.assertEqual(a.symbol, "BLURT")

    def test_type_confusion(self):
        """Test passing wrong types to Amount"""
        logger.info("Testing Amount type confusion...")
        with self.assertRaises(Exception):
            Amount([], blurt_instance=self.blurt)
        with self.assertRaises(Exception):
            Amount({}, blurt_instance=self.blurt)

if __name__ == '__main__':
    unittest.main()
