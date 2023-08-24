import os
import asyncio

from yeelight import Bulb

_BULB_IP = os.environ.get("BULB_IP")
_REPORT_URL = os.environ.get("REPORT_URL")


async def daemon():
    bulb = Bulb(_BULB_IP)
    on = False
    while True:
        on = not on

        if on:
            bulb.turn_on()
        else:
            bulb.turn_off()

        # # The daemon task will make an HTTP request every 10 seconds
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(_REPORT_URL)
        # print(response.json())
        await asyncio.sleep(5)
