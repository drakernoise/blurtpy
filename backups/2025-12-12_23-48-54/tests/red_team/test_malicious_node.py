import unittest
from unittest.mock import MagicMock, patch
from blurtpy import Blurt
from blurtpy.account import Account

class TestMaliciousNode(unittest.TestCase):
    def setUp(self):
        # Patch iscached to prevent recursion issues with mocks
        self.iscached_patcher = patch("blurtpy.blockchainobject.BlockchainObject.iscached", return_value=False)
        self.iscached_patcher.start()
        
        # Initialize Blurt in offline mode to avoid connection attempts
        self.blurt = Blurt(node=["https://fake-node.com"], offline=True)
        
        # Manually inject a MagicMock as the RPC interface
        self.blurt.rpc = MagicMock()
        
        # Prevent side effects from auxiliary calls
        self.blurt.rpc.get_use_appbase.return_value = False
        self.blurt.rpc.set_next_node_on_empty_reply.return_value = None
        
        # Mock network configuration so Asset("BLURT") works
        # We need to provide a valid chain_assets structure
        mock_network = {
            "chain_assets": [
                {"asset": "BLURT", "symbol": "BLURT", "precision": 3, "id": 0},
                {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 1}
            ],
            "prefix": "BLT"
        }
        # We patch get_network on the instance to return our mock config
        self.blurt.get_network = MagicMock(return_value=mock_network)

    def tearDown(self):
        self.iscached_patcher.stop()

    def test_fake_balance_injection(self):
        """Simulate that the node returns a fake/huge balance"""
        mock_response = [{
            "name": "victim",
            "balance": "1000000000.000 BLURT",
            "sbd_balance": "0.000 BLURT",
            "vesting_shares": "0.000000 VESTS",
            "created": "2020-01-01T00:00:00",
            "key_auths": []
        }]
        
        # Mock the specific method called by Account
        self.blurt.rpc.get_accounts.return_value = mock_response
        
        acc = Account("victim", blockchain_instance=self.blurt)
        acc.refresh()
        self.assertEqual(acc["balance"].amount, 1000000000.0)
        print("INFO: Library correctly processed the injected balance.")

    def test_malformed_json_response(self):
        """Simulate that the node returns garbage instead of valid JSON"""
        # Simulating get_accounts returning garbage
        self.blurt.rpc.get_accounts.return_value = 12345
        
        # Attempting to initialize (which calls refresh) should fail
        with self.assertRaises(Exception):
            Account("victim", blockchain_instance=self.blurt)

    def test_future_block_time(self):
        """Simulate that the node says we are in the year 3000"""
        mock_props = {
            "head_block_number": 1,
            "time": "3000-01-01T00:00:00",
            "current_witness": "evil_witness"
        }
        
        # Mock the specific method called by get_dynamic_global_properties
        self.blurt.rpc.get_dynamic_global_properties.return_value = mock_props
        
        props = self.blurt.get_dynamic_global_properties()
        self.assertIsNotNone(props, "get_dynamic_global_properties returned None")
        self.assertEqual(props['time'], "3000-01-01T00:00:00")
        print("INFO: Library accepted the future date.")

if __name__ == '__main__':
    unittest.main()
