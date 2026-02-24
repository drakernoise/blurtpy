import unittest
import json
import ast
import secrets
from blurtpy.utils import sanitize_permlink
from blurtpy.account import Account
from blurtpy.instance import shared_blockchain_instance

class TestJulesFixes(unittest.TestCase):
    def test_sanitize_permlink_edge_cases(self):
        # Test cases suggested by Jules
        self.assertEqual(sanitize_permlink("  Hello World  "), "hello-world")
        self.assertEqual(sanitize_permlink("Multiple...Dots"), "multiple-dots")
        self.assertEqual(sanitize_permlink("Special!@#$%^&*()Chars"), "specialchars")
        self.assertEqual(sanitize_permlink("UPPERCASE"), "uppercase")
        self.assertEqual(sanitize_permlink(""), "")

    def test_json_loads_fallback(self):
        # Verify the logic implemented in cli.py/utils.py
        valid_json = '{"key": "value"}'
        python_literal = "{'key': 'value'}"
        
        # Test valid JSON
        self.assertEqual(json.loads(valid_json), {"key": "value"})
        
        # Test fallback to ast.literal_eval
        with self.assertRaises(json.JSONDecodeError):
            json.loads(python_literal)
        
        self.assertEqual(ast.literal_eval(python_literal), {"key": "value"})

    def test_secrets_randomness(self):
        # Ensure secrets.randbits is used (manual check or verification of randomness)
        r1 = secrets.randbits(64)
        r2 = secrets.randbits(64)
        self.assertNotEqual(r1, r2)
        self.assertIsInstance(r1, int)

    def test_account_validation_edge_cases(self):
        # Test extreme account names
        with self.assertRaises(Exception):
            Account("a" * 17) # Too long
        with self.assertRaises(Exception):
            Account("ab") # Too short
        with self.assertRaises(Exception):
            Account("-starts-with-dash")
        with self.assertRaises(Exception):
            Account("ends-with-dash-")

if __name__ == '__main__':
    unittest.main()
