from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DailySelfReport(BaseModel):
    happiness: int
    tiredness: int

    notable_events: str
    notes: str


# Data Transfer Object
class DailySelfReportTransfer(BaseModel):
    report: DailySelfReport


# Data Storage Object
class DailySelfReportStorage(DailySelfReportTransfer):
    id: Optional[str] = None
    modified_timestamp: Optional[datetime] = None
    created_timestamp: Optional[datetime] = None


class TodayResponse(BaseModel):
    report: Optional[DailySelfReportStorage]
    error: Optional[str]


TODAY_MISSING_RESPONSE = TodayResponse(error="Report not found")
