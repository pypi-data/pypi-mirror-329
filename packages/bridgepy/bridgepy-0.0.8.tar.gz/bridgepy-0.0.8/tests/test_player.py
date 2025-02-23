from unittest import TestCase, main

from bridgepy.bid import Bid
from bridgepy.player import PlayerBid, PlayerId


class TestPlayer(TestCase):

    def test_PlayerBid(self):
        self.assertEqual(
            PlayerBid(player_id = PlayerId("1"), bid = Bid.from_string("1NT")),
            PlayerBid(player_id = PlayerId("1"), bid = Bid(level = 1, suit = None))
        )

if __name__ == '__main__':
    main()
