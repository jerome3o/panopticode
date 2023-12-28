from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import MONGODB_DATABASE, MONGODB_CONNECTION_STRING
from db.mongo import DailySelfReportMongoDB
from models import (
    DailySelfReportStorage,
    DailySelfReportTransfer,
    TodayResponse,
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


# todo dependency inject db client
@app.on_event("startup")
async def startup_db_client():
    print(MONGODB_CONNECTION_STRING, MONGODB_DATABASE)
    app.db_client = DailySelfReportMongoDB(
        MONGODB_CONNECTION_STRING,
        MONGODB_DATABASE,
    )


@app.on_event("shutdown")
async def shutdown_db_client():
    app.db_client.close()


@app.post("/reports/", response_model=DailySelfReportStorage)
async def create_report(record: DailySelfReportTransfer):
    return await app.db_client.create_report(record)


@app.get("/reports/", response_model=List[DailySelfReportStorage])
async def get_reports():
    return await app.db_client.get_reports()


@app.put("/reports/{id}/", response_model=DailySelfReportStorage)
async def update_report(id: str, record: DailySelfReportTransfer):
    # TODO(j.swannack): reconcile types
    return await app.db_client.update_report(id, record)


# Endpoint to check if there has been a report today
@app.get("/reports/today/", response_model=TodayResponse)
async def get_todays_record():
    return await app.db_client.get_todays_report()


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(app, host="0.0.0.0", port=8000)
