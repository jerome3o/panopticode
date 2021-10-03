import logging
from functools import wraps
from dataclasses import dataclass
from typing import Callable, Generic, List, Type, TypeVar

from bson.objectid import ObjectId
from pydantic import BaseModel, BaseSettings, Field
from pymongo import MongoClient
from pymongo.collection import Collection

from apitools.models.api import Crud, MongoModel

_logger = logging.getLogger(__name__)

_StoreT = TypeVar("_StoreT", bound=MongoModel)
_DtoT = TypeVar("_DtoT", bound=BaseModel)


class MongoSettings(BaseSettings):
    host: str = Field(env="MONGO_DB_HOST")
    port: int = Field(env="MONGO_DB_PORT", default=27017)
    username: str = Field(env="MONGO_DB_USERNAME")
    password: str = Field(env="MONGO_DB_PASSWORD")


def get_client(settings: MongoSettings = None):
    settings = settings or MongoSettings()
    return MongoClient(
        host=settings.host,
        port=settings.port,
        username=settings.username,
        password=settings.password,
    )


@dataclass
class Converter(Generic[_StoreT, _DtoT]):
    dto_model: Type[_DtoT]
    from_dto: Callable[[_DtoT], _StoreT]
    to_dto: Callable[[_StoreT], _DtoT]

def str_id(doc: dict) -> dict:
    return {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()}


def _object_id(doc: dict) -> dict:
    return {k: ObjectId(v) if k == "_id" else v for k, v in doc.items()}


def _id_filt(item_id: str):
    return {"_id": ObjectId(item_id)}


def _to_dict(item: _StoreT):
    return _object_id(item.dict())


class MongoCrud(Generic[_DtoT], Crud[_DtoT]):
    def __init__(
        self,
        model: Type[_StoreT],
        collection: Collection,
        dto_converter: Converter[_StoreT, _DtoT] = None,
    ):
        self._model: BaseModel = model
        self._collection = collection
        
        self._dto_model = dto_converter.dto_model if dto_converter is not None else self._model
        self._from_dto = dto_converter.from_dto if dto_converter is not None else (lambda x: x)
        self._to_dto = dto_converter.to_dto if dto_converter is not None else (lambda x: x)
    
    def _try_parse_dict(self, item: dict):
        try: 
            return self._model.parse_obj(str_id(item))
        except ValueError:
            _logger.exception(f"Failed to parse {self.model.__name__}: \n{item}")
            return None

    def get_all(self) -> List[_DtoT]:
        return list(
            filter(
                lambda x: x is not None,
                map(
                    lambda doc: self._to_dto(self._try_parse_dict(doc)),
                    self._collection.find({}),
                )
            )
        )

    def get(self, item_id: str) -> _DtoT:
        return self._to_dto(
            self._try_parse_dict(self._collection.find_one(_id_filt(item_id)))
        )

    def create(self, item: _DtoT) -> _DtoT:
        return self.get(
            str(self._collection.insert_one(_to_dict(self._from_dto(item))).inserted_id)
        )

    def idempotent_create(self, item: _DtoT) -> _DtoT:
        item_json = _to_dict(self._from_dto(item))
        result = self._collection.find_one_and_replace(
            filter=item_json,
            replacement=item_json,
            upsert=True,
        )
        result = result or self._collection.find_one(item_json)
        return self._to_dto(self._try_parse_dict(result))

    def update(self, item_id: str, item: _DtoT) -> _DtoT:
        return self._to_dto(
            self._try_parse_dict(
                self._collection.find_one_and_replace(
                    filter=_id_filt(item_id), replacement=_to_dict(self._from_dto(item))
                )
            )
        )

    def delete(self, item_id: str) -> int:
        return self._collection.delete_one(_id_filt(item_id)).deleted_count
