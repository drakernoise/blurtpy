import unittest
import importlib.metadata
import logging
from packaging import version

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAuditDependencies(unittest.TestCase):
    def test_ecdsa_version(self):
        """Verify ecdsa version is secure (>=0.13)"""
        v = importlib.metadata.version("ecdsa")
        logger.info(f"ecdsa version: {v}")
        self.assertTrue(version.parse(v) >= version.parse("0.13"),
                        "ecdsa version too old! Vulnerable to timing attacks.")

    def test_cryptography_version(self):
        """Verify cryptography version is recent"""
        v = importlib.metadata.version("cryptography")
        logger.info(f"cryptography version: {v}")
        self.assertTrue(version.parse(v) >= version.parse("3.0"),
                        "cryptography version too old.")

    def test_requests_version(self):
        """Verify requests version"""
        v = importlib.metadata.version("requests")
        logger.info(f"requests version: {v}")
        self.assertTrue(version.parse(v) >= version.parse("2.20"),
                        "requests version too old.")

if __name__ == "__main__":
    unittest.main()
