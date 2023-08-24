import asyncio
import os
import logging

import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from daemon import daemon

_logger = logging.getLogger(__name__)


class Status(BaseModel):
    status: str


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("hey")
    # This function will run the daemon task in the background when the server starts
    app.state.http_daemon_task = asyncio.create_task(_try_daemon())


@app.on_event("shutdown")
async def shutdown_event():
    # This function will cancel the daemon task when the server is shutting down
    app.state.http_daemon_task.cancel()


async def _try_daemon():
    while True:
        try:
            await daemon()
        except Exception:
            _logger.exception("Error in http daemon")


@app.get("/status", response_model=Status)
async def get_status():
    # Returning a mock status object
    return {"status": "up"}


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(app, host="0.0.0.0", port=8000)
