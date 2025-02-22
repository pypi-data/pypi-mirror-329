from unittest import TestCase, main

from bridgepy.card import Card, Deck, Rank, Suit


class TestCard(TestCase):
    
    def test_compare_Rank(self):
        self.assertTrue(Rank.ACE > Rank.TWO)
        self.assertTrue(Rank.KING < Rank.ACE)
        self.assertTrue(Rank.QUEEN == Rank.QUEEN)

    def test_compare_Suit(self):
        self.assertTrue(Suit.CLUB < Suit.HEART)
        self.assertTrue(Suit.HEART > Suit.DIAMOND)
        self.assertTrue(Suit.SPADE == Suit.SPADE)

    def test_compare_Card(self):
        self.assertTrue(Card(rank = Rank.ACE, suit = Suit.CLUB) < Card(rank = Rank.TWO, suit = Suit.DIAMOND))
        self.assertTrue(Card(rank = Rank.TWO, suit = Suit.SPADE) > Card(rank = Rank.ACE, suit = Suit.HEART))
        self.assertTrue(Card(rank = Rank.TWO, suit = Suit.SPADE) > Card(rank = Rank.ACE, suit = Suit.HEART))

    def test_from_string(self):
        self.assertEqual(Card.from_string("AS"), Card(rank = Rank.ACE, suit = Suit.SPADE))
        self.assertEqual(Card.from_string("10D"), Card(rank = Rank.TEN, suit = Suit.DIAMOND))

    def test_Deck(self):
        deck = Deck()
        self.assertEqual(len(set(deck.cards)), 52)

if __name__ == '__main__':
    main()
