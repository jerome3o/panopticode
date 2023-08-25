from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from auth import router as auth_router
from constants import SESSION_MIDDLEWARE_SECRET


app = FastAPI()

# Install the SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_MIDDLEWARE_SECRET,
)


app.include_router(auth_router, tags=["Authentication"])


# @app.get("/token/{token_id}")
# def read_token(token_id):
#     token = get_token(token_id)
#     if token is None:
#         raise HTTPException(status_code=404, detail="Token not found")
#     return token


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(app, host="127.0.0.1", port=8000)
