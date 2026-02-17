import sys
import os
import unittest

# Add the current directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blurtpy.utils import sanitize_permlink, assets_from_string, resolve_authorperm, load_dirty_json

class TestRegexOptimizations(unittest.TestCase):
    def test_sanitize_permlink(self):
        cases = [
            ("My Awesome Post", "my-awesome-post"),
            ("another_permlink.with_dots", "another-permlink-with-dots"),
            ("Complex!@#$%^&*()_+ Title", "complex--title"),
            ("   spaces   ", "spaces"),
            ("---already-sanitized---", "---already-sanitized---"),
            ("Mixed CASE Title", "mixed-case-title"),
            ("unicode é á î", "unicode---"), # Assuming we only want ASCII as per final step
            ("multiple...dots___underscores", "multiple---dots---underscores"),
        ]
        for input_str, expected in cases:
            result = sanitize_permlink(input_str)
            self.assertEqual(result, expected, f"Failed for {input_str}: expected {expected}, got {result}")

    def test_assets_from_string(self):
        self.assertEqual(assets_from_string("BLURT:VESTS"), ["BLURT", "VESTS"])
        self.assertEqual(assets_from_string("BLURT/VESTS"), ["BLURT", "VESTS"])
        self.assertEqual(assets_from_string("BLURT-VESTS"), ["BLURT", "VESTS"])

    def test_resolve_authorperm(self):
        self.assertEqual(resolve_authorperm("@username/permlink"), ("username", "permlink"))
        self.assertEqual(resolve_authorperm("username/permlink"), ("username", "permlink"))
        self.assertEqual(resolve_authorperm("https://blurtit.com/@username/permlink"), ("username", "permlink"))
        self.assertEqual(resolve_authorperm("https://d.tube/#!/v/username/permlink"), ("username", "permlink"))

    def test_load_dirty_json(self):
        dirty = "{'key': 'value', 'boolean': True, 'another': False, 'unicode': u'text'}"
        expected = {"key": "value", "boolean": True, "another": False, "unicode": "text"}
        self.assertEqual(load_dirty_json(dirty), expected)

if __name__ == "__main__":
    unittest.main()
