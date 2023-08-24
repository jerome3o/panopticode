import os
import asyncio
import logging
import httpx

from yeelight import Bulb

_BULB_IP = os.environ.get("BULB_IP")
_REPORT_URL = os.environ.get("REPORT_URL")

_logger = logging.getLogger(__name__)


async def has_reported_today():
    async with httpx.AsyncClient() as client:
        response = await client.get(_REPORT_URL)

    return response.json().get("value") is not None


async def daemon():
    bulb = Bulb(_BULB_IP)
    while True:
        _logger.info("Checking if reported today")
        reported_today = await has_reported_today()
        _logger.info(f"Reported today: {reported_today}")

        if not reported_today:
            bulb.turn_on()
        else:
            bulb.turn_off()

        await asyncio.sleep(5)
