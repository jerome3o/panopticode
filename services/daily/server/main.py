from datetime import datetime

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from server.models import DailySelfReportStorage, DailySelfReportTransfer


app = FastAPI()

# TODO(j.swannack): api keys


# todo dependency inject db client
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient('<your-mongodb-connection-string>')
    app.mongodb = app.mongodb_client['<your-database-name>']


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
    today = datetime.now().date()
    result = await app.mongodb['daily_self_report'].find_one({'created_timestamp': {'$gte': today}})
    if result:
        return DailySelfReportStorage.model_validate(result)
    else:
        # 404
        return None
