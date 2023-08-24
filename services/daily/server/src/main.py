from datetime import datetime, time
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from models import (
    DailySelfReportStorage,
    DailySelfReportTransfer,
    TodayResponse,
    TODAY_MISSING_RESPONSE,
)


app = FastAPI()

# allow CORS
# todo: tighten this up
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO(j.swannack): api keys

_MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")
_MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE")


# todo dependency inject db client
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(_MONGODB_CONNECTION_STRING)
    app.mongodb = app.mongodb_client[_MONGODB_DATABASE]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.post("/reports/", response_model=DailySelfReportStorage)
async def create_record(record: DailySelfReportTransfer):
    storage_record = DailySelfReportStorage.model_validate(record.model_dump())
    storage_record.modified_timestamp = datetime.now()
    storage_record.created_timestamp = datetime.now()
    result = await app.mongodb["daily_self_report"].insert_one(
        storage_record.model_dump()
    )
    storage_record.id = str(result.inserted_id)
    return storage_record


@app.put("/reports/{id}/", response_model=DailySelfReportStorage)
async def update_record(id: str, record: DailySelfReportTransfer):
    storage_record = DailySelfReportStorage.model_validate(record.model_dump())
    storage_record.modified_timestamp = datetime.now()

    result = await app.mongodb["daily_self_report"].update_one(
        {"_id": ObjectId(id)}, {"$set": storage_record.model_dump()}
    )

    if result.modified_count:
        storage_record.id = id
        return storage_record
    return None


# Endpoint to check if there has been a report today
@app.get("/reports/today/", response_model=TodayResponse)
async def get_today_record():
    today = datetime.combine(datetime.now().date(), time())
    result = await app.mongodb["daily_self_report"].find_one(
        {"created_timestamp": {"$gte": today}}
    )
    if result:
        return TodayResponse(value=result)
    return TODAY_MISSING_RESPONSE


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(app, host="0.0.0.0", port=8000)