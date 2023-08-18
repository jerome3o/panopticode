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
    id: Optional[str]
    modified_timestamp: Optional[datetime]
    created_timestamp: Optional[datetime]
