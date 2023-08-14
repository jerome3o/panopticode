import os
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader


app = FastAPI()
api_keys = set(os.environ.get("API_KEYS", "").split(","))
api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@app.get("/protected")
def protected_route(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
