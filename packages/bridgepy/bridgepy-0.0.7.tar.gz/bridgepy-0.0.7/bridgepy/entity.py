from dataclasses import dataclass
from typing import Generic, TypeVar


EntityId = TypeVar("EntityId")

@dataclass
class Entity(Generic[EntityId]):
    id: EntityId
