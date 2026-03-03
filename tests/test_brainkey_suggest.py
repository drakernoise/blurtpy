import unittest

from blurtgraphenebase.account import BrainKey, BrainKeyDictionary


class TestBrainKeySuggest(unittest.TestCase):
    def test_suggest_returns_words_from_dictionary(self):
        phrase = BrainKey().suggest(word_count=32)
        words = phrase.split(' ')

        self.assertEqual(len(words), 32)

        dictionary_words = {w.upper() for w in BrainKeyDictionary.split(',')}
        self.assertTrue(all(word in dictionary_words for word in words))


if __name__ == '__main__':
    unittest.main()
