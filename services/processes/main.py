import os
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
import psutil


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


@app.get("/ps")
def psaux(api_key: str = Security(get_api_key)):
    # Iterate over all running process
    procs = []
    for proc in psutil.process_iter(["pid", "name", "username"]):
        info = proc.info
        procs.append(
            {
                "pid": info["pid"],
                "name": info["name"],
                "username": info["username"],
            }
        )
    return procs


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
