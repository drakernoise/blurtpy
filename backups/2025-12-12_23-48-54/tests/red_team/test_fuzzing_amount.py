import unittest
from blurtpy.amount import Amount

class TestAmountFuzzing(unittest.TestCase):
    def test_overflow_huge_string(self):
        """Attempt overflow with huge string"""
        # 10,000 characters of "1"
        huge_str = "1" * 10000 + " BLURT"
        
        # We expect the library to handle this (probably ValueError or accept it if Python supports it)
        # Python supports arbitrarily large integers, so it might accept it.
        # The important thing is that it does NOT crash with SegFault or uncontrolled MemoryError.
        try:
            a = Amount(huge_str)
            print(f"INFO: Amount accepted a number with {len(huge_str)} digits.")
        except ValueError:
            print("INFO: Amount correctly rejected the huge string.")
        except Exception as e:
            self.fail(f"CRASH: Uncontrolled exception: {e}")

    def test_malformed_assets(self):
        """Fuzzing with invalid assets"""
        malformed = [
            "10.000 @@000000013", # Symbol UUID
            "10.000 \x00\x00\x00", # Null bytes
            "10.000 <script>alert(1)</script>", # XSS attempt
            "NaN BLURT",
            "Infinity BLURT"
        ]
        
        for s in malformed:
            with self.assertRaises((ValueError, TypeError), msg=f"Should reject {s}"):
                Amount(s)

if __name__ == '__main__':
    unittest.main()
