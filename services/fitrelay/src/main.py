from fastapi import FastAPI, HTTPException
from auth import router as auth_router
from db import get_token

app = FastAPI()

app.include_router(auth_router, tags=["Authentication"])


@app.get("/token/{token_id}")
def read_token(token_id):
    token = get_token(token_id)
    if token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    return token


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(app, host="127.0.0.1", port=8000)
