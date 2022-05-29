from dataclasses import dataclass

from ...consts.types import Position


@dataclass(unsafe_hash=True, frozen=True)
class SearchState:
    position: Position

    def __lt__(self, other: "SearchState") -> bool:
        return self.position < other.position


@dataclass(unsafe_hash=True, frozen=True)
class FourPointState(SearchState):
    bit_mask: int = 0b0000

    def __lt__(self, other: "FourPointState") -> bool:
        return self.bit_mask > other.bit_mask


@dataclass(unsafe_hash=True, frozen=True)
class AllFoodState(SearchState):
    rest: frozenset[Position]

    def __lt__(self, other: "AllFoodState") -> bool:
        return len(self.rest) < len(other.rest)
