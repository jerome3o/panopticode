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
    def get_all() -> List[dto_class]:
        return api.get_all()

    @app.get(endpoint_base + "/{item_id}", response_model=dto_class)
    def get(item_id: str) -> dto_class:
        return api.get()

    @app.post(endpoint_base, response_model=dto_class)
    def create(item: dto_class) -> dto_class:
        return api.create()

    @app.put(endpoint_base, response_model=dto_class)
    def idempotent_create(item: dto_class) -> dto_class:
        return api.idempotent_create()

    @app.post(endpoint_base + "/{item_id}", response_model=dto_class)
    def update(item_id: str, item: dto_class) -> dto_class:
        return api.update()

    @app.delete(endpoint_base + "/{item_id}", response_model=int)
    def delete(item_id: str) -> int:
        return api.delete()

