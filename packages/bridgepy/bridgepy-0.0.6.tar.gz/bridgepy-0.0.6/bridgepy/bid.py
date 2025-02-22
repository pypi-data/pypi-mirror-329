from dataclasses import dataclass
from functools import total_ordering
from typing import Optional

from bridgepy.card import Suit


@total_ordering
@dataclass
class Bid:
    level: int
    suit: Optional[Suit]

    def __lt__(self, other) -> bool:
        if not isinstance(other, Bid):
            return NotImplemented
        return (self.level, self.suit is None, self.suit) < (other.level, other.suit is None, other.suit)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Bid):
            return NotImplemented
        return (self.level, self.suit) == (other.level, other.suit)

    def __repr__(self) -> str:
        level_str = str(self.level)
        suit_str = self.suit.value if self.suit is not None else "NT"
        return f"{level_str}{suit_str}"

    @classmethod
    def from_string(cls, bid_str: str):
        level = bid_str[:1]
        suit = bid_str[1:]
        if suit == "NT":
            suit = None
        return cls(level = int(level), suit = Suit(suit) if suit is not None else suit)
