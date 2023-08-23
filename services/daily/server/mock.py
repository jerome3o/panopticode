from datetime import datetime, time
from fastapi import FastAPI, HTTPException

from models import DailySelfReportStorage, DailySelfReportTransfer

app = FastAPI()

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
    return _make_fake_storage_object(record)


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
        return report

    raise HTTPException(status_code=404, detail="Record not found")
