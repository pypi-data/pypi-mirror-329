from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from random import shuffle


@total_ordering
class Rank(str, Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    def __hash__(self) -> int:
        return hash(self.value)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        return _rank_order[self.value] < _rank_order[other.value]
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        return _rank_order[self.value] == _rank_order[other.value]

_rank_order = {rank.value: i for i, rank in enumerate(Rank)}

@total_ordering
class Suit(str, Enum):
    CLUB = "C"
    DIAMOND = "D"
    HEART = "H"
    SPADE = "S"

    def __hash__(self) -> int:
        return hash(self.value)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Suit):
            return NotImplemented
        return _suit_order[self.value] < _suit_order[other.value]
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Suit):
            return NotImplemented
        return _suit_order[self.value] == _suit_order[other.value]

_suit_order = {rank.value: i for i, rank in enumerate(Suit)}

@total_ordering
@dataclass
class Card:
    rank: Rank
    suit: Suit

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __lt__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (self.suit, self.rank) < (other.suit, other.rank)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (self.suit, self.rank) == (other.suit, other.rank)

    def __repr__(self) -> str:
        return f"{self.rank.value}{self.suit.value}"

    @classmethod
    def from_string(cls, card_str: str):
        rank = card_str[:-1]
        suit = card_str[-1:]
        return cls(rank = Rank(rank), suit = Suit(suit))

class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = [Card(rank = rank, suit = suit) for rank in Rank for suit in Suit]
        shuffle(self.cards)
