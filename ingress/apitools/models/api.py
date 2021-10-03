from typing import Generic, TypeVar, List, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class MongoModel(BaseModel):
    db_id: Optional[str] = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True


Dto = TypeVar("Dto", bound=BaseModel)


class Crud(Generic[Dto], ABC):

    @abstractmethod
    def get_all(self) -> List[Dto]:
        pass

    @abstractmethod
    def get(self, item_id: str) -> Dto:
        pass

    @abstractmethod
    def create(self, item: Dto) -> Dto:
        pass

    @abstractmethod
    def idempotent_create(self, item: Dto) -> Dto:
        pass

    @abstractmethod
    def update(self, item_id: str, item: Dto) -> Dto:
        pass

    @abstractmethod
    def delete(self, item_id: str) -> int:
        pass
