from datetime import datetime, time
import os

from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from server.models import DailySelfReportStorage, DailySelfReportTransfer


app = FastAPI()

# TODO(j.swannack): api keys

_MONGODB_CONNECTION_STRING = os.environ.get('MONGODB_CONNECTION_STRING')
_MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE')

# todo dependency inject db client
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(_MONGODB_CONNECTION_STRING)
    app.mongodb = app.mongodb_client[_MONGODB_DATABASE]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.post("/records/", response_model=DailySelfReportStorage)
async def create_record(record: DailySelfReportTransfer):
    storage_record = DailySelfReportStorage.model_validate(record.model_dump())
    storage_record.modified_timestamp = datetime.now()
    result = await app.mongodb['daily_self_report'].insert_one(storage_record.model_dump())
    storage_record.id = str(result.inserted_id)
    return storage_record


# Endpoint to check if there has been a report today
@app.get("/records/today/", response_model=DailySelfReportStorage)
async def get_today_record():
    today = datetime.combine(datetime.now().date(), time())
    result = await app.mongodb['daily_self_report'].find_one({'created_timestamp': {'$gte': today}})
    if result:
        return DailySelfReportStorage.model_validate(result)
    else:
        # raise 404
        raise HTTPException(status_code=404, detail="Record not found")
