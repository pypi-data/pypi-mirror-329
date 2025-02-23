from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bridgepy.entity import Entity, EntityId


EntityType = TypeVar("EntityType", bound = Entity)

class Datastore(ABC, Generic[EntityId, EntityType]):

    @abstractmethod
    def insert(self, entity: EntityType) -> None:
        pass
    
    @abstractmethod
    def update(self, entity: EntityType) -> None:
        pass

    @abstractmethod
    def delete(self, id: EntityId) -> None:
        pass

    @abstractmethod
    def query(self, id: EntityId) -> EntityType | None:
        pass
