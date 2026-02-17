import unittest
import time
import threading
from blurtpy import Blurt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestStress(unittest.TestCase):
    def setUp(self):
        # Use hardcoded nodes
        self.nodes = ["https://rpc.beblurt.com", "https://blurt-rpc.saboin.com"]
        self.blurt = Blurt(node=self.nodes)

    def test_rate_limiting_simulation(self):
        """Simulate a burst of read requests to test stability"""
        logger.info("Testing rate limiting / burst requests...")
        
        success_count = 0
        failure_count = 0
        total_requests = 20
        
        start_time = time.time()
        
        for i in range(total_requests):
            try:
                # Lightweight call
                self.blurt.get_dynamic_global_properties()
                success_count += 1
            except Exception as e:
                logger.warning(f"Request {i} failed: {e}")
                failure_count += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"Completed {total_requests} requests in {duration:.2f}s")
        logger.info(f"Success: {success_count}, Failure: {failure_count}")
        
        # We expect most to succeed, but some might fail due to actual node rate limits.
        # The test passes if the library itself doesn't crash.
        self.assertGreater(success_count, 0, "Should have at least some successful requests")

    def test_node_failover_simulation(self):
        """Simulate node failure by providing a bad node first"""
        logger.info("Testing node failover...")
        
        # First node is bad, second is good
        mixed_nodes = ["https://bad-node.example.com", "https://rpc.beblurt.com"]
        blurt_failover = Blurt(node=mixed_nodes, num_retries=2)
        
        try:
            props = blurt_failover.get_dynamic_global_properties()
            self.assertIsNotNone(props)
            logger.info("Failover successful: Fetched properties despite bad first node.")
        except Exception as e:
            self.fail(f"Failover failed: {e}")

if __name__ == '__main__':
    unittest.main()
