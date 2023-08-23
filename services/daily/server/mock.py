from datetime import datetime, time
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import (
    DailySelfReportStorage,
    DailySelfReportTransfer,
    TodayResponse,
    TODAY_MISSING_RESPONSE,
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


data = {}


# pre-defined data for testing
def _make_fake_storage_object(
    record: DailySelfReportTransfer,
) -> DailySelfReportStorage:
    _id = str(len(data) + 1)
    return DailySelfReportStorage(
        id=_id,
        report=record.report.model_dump(),
        created_timestamp=datetime.now(),
        modified_timestamp=datetime.now(),
    )


@app.post("/reports/", response_model=DailySelfReportStorage)
async def create_record(record: DailySelfReportTransfer):
    # just return predefined data regardless of input

    record = _make_fake_storage_object(record)
    data[record.id] = record
    return record


@app.get("/reports/today/", response_model=DailySelfReportStorage)
async def get_today_record():
    today = datetime.combine(datetime.now().date(), time())

    report = next(
        (
            report
            for report in data.values()
            if report.created_timestamp.date() == today.date()
        ),
        None,
    )

    if report:
        return TodayResponse(report=report)

    return TODAY_MISSING_RESPONSE


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
