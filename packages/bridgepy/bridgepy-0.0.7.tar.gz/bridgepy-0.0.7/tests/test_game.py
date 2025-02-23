from unittest import TestCase, main

from bridgepy.bid import Bid
from bridgepy.card import Card, Rank, Suit
from bridgepy.exception import GameAlready4Players, GameAlreadyDealtException, GameAlreadyFinishedException, GameAuctionAlreadyFinishedException,\
    GameAuctionNotFinishedException, GamePlayerAlreadyAdded, GameInvalidBidException, GameInvalidBidStateException, GameNotBidWinner,\
    GameNotPlayerBidTurnException, GameNotPlayerTrickTurnException, GameNotReadyToDealYetException,\
    GameInvalidPlayerTrickException
from bridgepy.game import Game, GameId, GameTrick
from bridgepy.player import PlayerBid, PlayerHand, PlayerId, PlayerTrick


class TestPlayer(TestCase):

    def test_constructor(self):
        self.assertEqual(Game(id = GameId("1"), player_ids = [PlayerId("111")]), Game(**{"id": GameId("1"), "player_ids": [PlayerId("111")]}))

    def test_GameAlready4Players(self):
        with self.assertRaises(GameAlready4Players):
            game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
            game.add_player(PlayerId("222"))
            game.add_player(PlayerId("333"))
            game.add_player(PlayerId("444"))
            game.add_player(PlayerId("555"))

    def test_GameDuplicatePlayers(self):
        with self.assertRaises(GamePlayerAlreadyAdded):
            game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
            game.add_player(PlayerId("111"))
    
    def test_ready_to_deal(self):
        game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
        game.add_player(PlayerId("222"))
        game.add_player(PlayerId("333"))
        game.add_player(PlayerId("444"))
        self.assertTrue(game.ready_to_deal())

    def test_dealt(self):
        game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
        game.add_player(PlayerId("222"))
        game.add_player(PlayerId("333"))
        game.add_player(PlayerId("444"))
        self.assertTrue(game.dealt())

        for player_hand in game.player_hands:
            cards = player_hand.cards
            self.assertEqual(len(cards), 13)
            for i in range(len(cards) - 1):
                self.assertTrue(cards[i] > cards[i + 1])
        nested_list = [player_hand.cards for player_hand in game.player_hands]
        flattened = [item for sublist in nested_list for item in sublist]
        self.assertEqual(len(set(flattened)), 52)

    def test_GameNotReadyToDealYetException(self):
        with self.assertRaises(GameNotReadyToDealYetException):
            game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
            game.add_player(PlayerId("222"))
            game.add_player(PlayerId("333"))
            game.deal()

    def test_GameAlreadyDealtException(self):
        with self.assertRaises(GameAlreadyDealtException):
            game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
            game.add_player(PlayerId("222"))
            game.add_player(PlayerId("333"))
            game.add_player(PlayerId("444"))
            game.deal()
    
    def test_next_bid_player_id(self):
        game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
        game.add_player(PlayerId("222"))
        game.add_player(PlayerId("333"))
        game.add_player(PlayerId("444"))
        self.assertEqual(game.next_bid_player_id(), PlayerId("222"))
        game.bids.append(PlayerBid(player_id = PlayerId("222"), bid = Bid(level = 1, suit = Suit.CLUB)))
        self.assertEqual(game.next_bid_player_id(), PlayerId("333"))
        game.bids.append(PlayerBid(player_id = PlayerId("333"), bid = None))
        self.assertEqual(game.next_bid_player_id(), PlayerId("444"))
        game.bids.append(PlayerBid(player_id = PlayerId("444"), bid = Bid(level = 1, suit = None)))
        self.assertEqual(game.next_bid_player_id(), PlayerId("111"))

    def test_GameNotPlayerBidTurnException(self):
        with self.assertRaises(GameNotPlayerBidTurnException):
            game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
            game.add_player(PlayerId("222"))
            game.add_player(PlayerId("333"))
            game.add_player(PlayerId("444"))
            player_id = PlayerId("111")
            game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("1NT")))

    def test_GameInvalidBidException(self):
        game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
        game.add_player(PlayerId("222"))
        game.add_player(PlayerId("333"))
        game.add_player(PlayerId("444"))

        with self.assertRaises(GameInvalidBidException):
            player_id = game.next_bid_player_id()
            game.bid(PlayerBid(player_id = player_id, bid = None))

        player_id = game.next_bid_player_id()
        game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("1NT")))

        with self.assertRaises(GameInvalidBidException):
            player_id = game.next_bid_player_id()
            game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("1NT")))

        player_id = game.next_bid_player_id()
        game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("2S")))

        with self.assertRaises(GameInvalidBidException):
            player_id = game.next_bid_player_id()
            game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("2H")))

    def test_GameInvalidBidStateException(self):
        with self.assertRaises(GameInvalidBidStateException):
            game = Game(id = GameId("1"), player_ids = [])
            game.last_player_bid()

    def test_GameAuctionAlreadyFinishedException(self):
        with self.assertRaises(GameAuctionAlreadyFinishedException):
            game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
            game.add_player(PlayerId("222"))
            game.add_player(PlayerId("333"))
            game.add_player(PlayerId("444"))
            player_id = game.next_bid_player_id()
            game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("1NT")))
            for _ in range(4):
                player_id = game.next_bid_player_id()
                game.bid(PlayerBid(player_id = player_id, bid = None))
    
    def test_GameNotBidWinner(self):
        with self.assertRaises(GameNotBidWinner):
            game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
            game.add_player(PlayerId("222"))
            game.add_player(PlayerId("333"))
            game.add_player(PlayerId("444"))
            player_id = game.next_bid_player_id()
            game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("1NT")))
            for _ in range(3):
                player_id = game.next_bid_player_id()
                game.bid(PlayerBid(player_id = player_id, bid = None))
            game.choose_partner(PlayerId("111"), Card.from_string("AC"))
    
    def test_choose_partner(self):
        game = Game(id = GameId("1"), player_ids = [PlayerId("111")])
        game.add_player(PlayerId("222"))
        game.add_player(PlayerId("333"))
        game.add_player(PlayerId("444"))
        player_id = game.next_bid_player_id()
        game.bid(PlayerBid(player_id = player_id, bid = Bid.from_string("1NT")))
        for _ in range(3):
            player_id = game.next_bid_player_id()
            game.bid(PlayerBid(player_id = player_id, bid = None))
        game.choose_partner(game.bid_winner().player_id, Card.from_string("AC"))
        self.assertEqual(game.partner, Card(rank = Rank.ACE, suit = Suit.CLUB))
        self.assertEqual(game.partner.suit, Suit.CLUB)

    def test_GameAuctionNotFinishedException(self):
        with self.assertRaises(GameAuctionNotFinishedException):
            game = Game(id = GameId("1"), player_ids = [])
            game.bid_winner()

    def test_GameAlreadyFinishedException(self):
        with self.assertRaises(GameAlreadyFinishedException):
            game = Game(
                id = GameId("1"),
                player_ids = [],
                tricks = [GameTrick(player_tricks = [PlayerTrick(player_id = PlayerId("111"), trick = Card.from_string("AS"))] * 4)] * 13
            )
            game.next_trick_player_id()

    def test_GameNotPlayerTrickTurnException(self):
        with self.assertRaises(GameNotPlayerTrickTurnException):
            game = Game(
                id = GameId("1"),
                player_ids = [PlayerId("111"), PlayerId("222"), PlayerId("333"), PlayerId("444")],
                bids = [
                    PlayerBid(player_id = PlayerId("111"), bid = Bid.from_string("1C")),
                    PlayerBid(player_id = PlayerId("222"), bid = None),
                    PlayerBid(player_id = PlayerId("333"), bid = None),
                    PlayerBid(player_id = PlayerId("444"), bid = None)
                ]
            )
            game.trick(PlayerTrick(player_id = PlayerId("111"), trick = Card.from_string("AS")))

    def test_GamePlayerCardNotBelongToThemException(self):
        with self.assertRaises(GameInvalidPlayerTrickException):
            game = Game(
                id = GameId("1"),
                player_ids = [PlayerId("111"), PlayerId("222"), PlayerId("333"), PlayerId("444")],
                bids = [
                    PlayerBid(player_id = PlayerId("111"), bid = Bid.from_string("1C")),
                    PlayerBid(player_id = PlayerId("222"), bid = None),
                    PlayerBid(player_id = PlayerId("333"), bid = None),
                    PlayerBid(player_id = PlayerId("444"), bid = None),
                ],
                player_hands = [
                    PlayerHand(player_id = PlayerId("222"), cards = [Card.from_string("AC")]),
                ]
            )
            game.trick(PlayerTrick(player_id = PlayerId("222"), trick = Card.from_string("AS")))

    def test_scores(self):
        game = Game(id = GameId("1"), player_ids = [PlayerId("111"), PlayerId("222"), PlayerId("333"), PlayerId("444")])
        self.assertEqual(len(game.scores()), 4)
        for player_score in game.scores():
            self.assertEqual(player_score.score, 0)

if __name__ == '__main__':
    main()
