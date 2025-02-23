from unittest import TestCase, main

from bridgepy.bid import Bid
from bridgepy.card import Suit


class TestBid(TestCase):

    def test_constructor(self):
        self.assertEqual(Bid(level = 1, suit = Suit.CLUB), Bid(**{"level": 1, "suit": Suit.CLUB}))
        self.assertEqual(Bid(level = 1, suit = None), Bid(**{"level": 1, "suit": None}))

    def test_from_string(self):
        self.assertEqual(Bid.from_string("1C"), Bid(level = 1, suit = Suit.CLUB))
        self.assertEqual(Bid.from_string("7NT"), Bid(level = 7, suit = None))
    
    def test_compare(self):
        self.assertTrue(Bid(level = 1, suit = None) > Bid(level = 1, suit = Suit.SPADE))
        self.assertTrue(Bid(level = 2, suit = Suit.CLUB) > Bid(level = 1, suit = None))
        self.assertTrue(Bid(level = 4, suit = Suit.DIAMOND) < Bid(level = 4, suit = Suit.HEART))
        self.assertTrue(Bid(level = 4, suit = Suit.SPADE) == Bid(level = 4, suit = Suit.SPADE))

if __name__ == '__main__':
    main()
