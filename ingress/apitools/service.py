from typing import Type, List
from fastapi import FastAPI
from apitools.models.api import Crud, Dto


def configure_api(
    app: FastAPI, 
    api: Crud, 
    dto_class: Type[Dto],
    endpoint_base: str,
) -> None:
    @app.get(endpoint_base, response_model=List[dto_class])
    def get_all(self) -> List[dto_class]:
        return api.get_all()

    @app.get(endpoint_base + "/{item_id}", response_model=dto_class)
    def get(self, item_id: str) -> dto_class:
        return api.get()

    @app.post(endpoint_base, response_model=dto_class)
    def create(self, item: dto_class) -> dto_class:
        return api.create()

    @app.put(endpoint_base, response_model=dto_class)
    def idempotent_create(self, item: dto_class) -> dto_class:
        return api.idempotent_create()

    @app.post(endpoint_base + "/{item_id}", response_model=dto_class)
    def update(self, item_id: str, item: dto_class) -> dto_class:
        return api.update()

    @app.delete(endpoint_base + "/{item_id}", response_model=int)
    def delete(self, item_id: str) -> int:
        return api.delete()

