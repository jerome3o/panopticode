from typing import List
from pydantic import BaseModel
from ingress.models.api import MongoModel
from ingress.mongodb import get_client, MongoCrud


class TestNestedModel(BaseModel):
    test_3: str


class TestModel(MongoModel):
    test_1: str
    test_2: List[TestNestedModel]


client = get_client()
collection = client["test_db"]["test_collection"]

crud = MongoCrud[TestModel](TestModel, collection)

item = TestModel(
    test_1="value_1",
    test_2=[
        TestNestedModel(test_3="hello"),
        TestNestedModel(test_3="goodbye"),
    ]
)

db_item = crud.idempotent_create(item)
print(db_item)