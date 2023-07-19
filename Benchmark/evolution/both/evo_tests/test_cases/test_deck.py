import unittest
from dealer.deck import Deck

class TestDeck(unittest.TestCase):
    def test_make_deck_size(self):
        self.assertEqual(122, len(Deck.make_deck().loc))