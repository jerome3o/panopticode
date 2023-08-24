import asyncio
import os

import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from yeelight import Bulb


_REPORT_URL = os.environ.get("REPORT_URL")
_BULB_IP = os.environ.get("BULB_IP")


class Status(BaseModel):
    status: str


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("hey")
    # This function will run the daemon task in the background when the server starts
    app.state.http_daemon_task = asyncio.create_task(http_daemon())


@app.on_event("shutdown")
async def shutdown_event():
    # This function will cancel the daemon task when the server is shutting down
    app.state.http_daemon_task.cancel()


async def http_daemon():
    bulb = Bulb(_BULB_IP)
    on = False
    while True:
        on = not on

        print(on)

        if on:
            bulb.turn_on()
        else:
            bulb.turn_off()

        # # The daemon task will make an HTTP request every 10 seconds
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(_REPORT_URL)
        # print(response.json())
        await asyncio.sleep(5)


@app.get("/status", response_model=Status)
async def get_status():
    # Returning a mock status object
    return {"status": "up"}


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(app, host="0.0.0.0", port=8000)
