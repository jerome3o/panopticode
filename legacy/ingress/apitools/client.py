from typing import Generic, List, Type
import json
from apitools.models.api import Crud, Dto
from apitools.models.http import HttpClient, RequestsHttpClient


def from_raw(value: str) -> dict:
    return json.loads(value)


def to_raw(value: dict) -> str:
    return json.dumps(value, indent=4)


class HttpCrudClient(Crud[Dto], Generic[Dto]):
    def __init__(self, base_url: str, model: Type[Dto], http_client: HttpClient = None):
        self._model = model
        self._base_url = base_url.rstrip("/")
        self.http_client = http_client or RequestsHttpClient()

    def _to_dict(self, value: Dto) -> dict:
        return value.dict()

    def _from_dict(self, value: dict) -> Dto:
        return self._model.parse_obj(value)

    def get_all(self) -> List[Dto]:
        return list(
            map(self._from_dict, from_raw(self.http_client.get(self._base_url).body))
        )

    def get(self, item_id: str) -> Dto:
        return self._from_dict(
            from_raw(self.http_client.get(self._base_url + f"/{item_id}").body)
        )

    def create(self, item: Dto) -> Dto:
        return self._from_dict(
            from_raw(
                self.http_client.post(
                    self._base_url, data=to_raw(self._to_dict(item))
                ).body
            )
        )

    def idempotent_create(self, item: Dto) -> Dto:
        return self._from_dict(
            from_raw(
                self.http_client.put(
                    self._base_url, data=to_raw(self._to_dict(item))
                ).body
            )
        )

    def update(self, item_id: str, item: Dto) -> Dto:
        return self._from_dict(
            from_raw(
                self.http_client.post(
                    self._base_url + f"/{item_id}", data=to_raw(self._to_dict(item))
                ).body
            )
        )

    def delete(self, item_id: str) -> int:
        return from_raw(self.http_client.delete(self._base_url + f"/{item_id}").body)
