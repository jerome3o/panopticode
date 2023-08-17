from pydantic import BaseModel
from datetime import datetime


class DailyReport(BaseModel):
    date: datetime

    happiness: int
    tiredness: int

    notable_events: str
    notes: str
