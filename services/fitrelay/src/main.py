import os
from typing import List

from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from starlette.middleware.sessions import SessionMiddleware

from auth import router as auth_router
from constants import SESSION_MIDDLEWARE_SECRET
from db import create_db_if_needed, get_all_tokens_from_db
from models import TokenInfo


app = FastAPI()

api_keys = set(os.environ.get("PANOPTICODE_API_KEYS", "").split(","))
api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


# Install the SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_MIDDLEWARE_SECRET,
)


app.include_router(auth_router, tags=["Authentication"])


# on app start up create the db if needed
@app.on_event("startup")
def startup_event():
    create_db_if_needed()


@app.get("/token/", response_model=List[TokenInfo])
def read_token(api_key: str = Security(get_api_key)) -> List[TokenInfo]:
    token = get_all_tokens_from_db()
    if token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    return token


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(app, host="127.0.0.1", port=8000)
