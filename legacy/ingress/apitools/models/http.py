from typing import Any
from abc import ABC, abstractmethod
from functools import wraps

from pydantic import BaseModel
import requests


class HttpResponse(BaseModel):
    status_code: int
    body: str
    raw: Any


class HttpClient(ABC):
    @abstractmethod
    def get(self, url, data=None, params=None, headers=None) -> HttpResponse:
        pass

    @abstractmethod
    def post(self, url, data=None, params=None, headers=None) -> HttpResponse:
        pass

    @abstractmethod
    def put(self, url, data=None, params=None, headers=None) -> HttpResponse:
        pass

    @abstractmethod
    def delete(self, url, data=None, params=None, headers=None) -> HttpResponse:
        pass


def _catch_connection_error(operation: str): 
    def decorator(f):
        @wraps(f)
        def wrapper(self, url, data=None, params=None, headers=None):
            try:
                return f(self, url, data=data, params=params, headers=headers)
            except Exception as e:
                raise ConnectionError(
                    f'Failed to perform a "{operation}" request on {url}'
                ) from e
        return wrapper
    return decorator


class RequestsHttpClient(HttpClient):
    @_catch_connection_error("GET")
    def get(self, url: str, data=None, params: dict = None, headers: dict = None):
        res = requests.get(url, data=data, params=params, headers=headers)
        return HttpResponse(status_code=res.status_code, body=res.content.decode("utf-8"), raw=res)

    @_catch_connection_error("POST")
    def post(self, url: str, data=None, params: dict = None, headers: dict = None):
        res = requests.post(url, data=data, params=params, headers=headers)
        return HttpResponse(status_code=res.status_code, body=res.content.decode("utf-8"), raw=res)

    @_catch_connection_error("PUT")
    def put(self, url: str, data=None, params: dict = None, headers: dict = None):
        res = requests.put(url, data=data, params=params, headers=headers)
        return HttpResponse(status_code=res.status_code, body=res.content.decode("utf-8"), raw=res)

    @_catch_connection_error("DELETE")
    def delete(self, url: str, data=None, params: dict = None, headers: dict = None):
        res = requests.delete(url, data=data, params=params, headers=headers)
        return HttpResponse(status_code=res.status_code, body=res.content.decode("utf-8"), raw=res)
