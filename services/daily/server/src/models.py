from typing import Optional, Union, Annotated
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId


def bson_id_to_str(v: Optional[Union[str, ObjectId]]) -> Optional[str]:
    if v is not None:
        return str(v)
    return v


BsonId = Annotated[Optional[str], BeforeValidator(bson_id_to_str)]


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
    id: BsonId = Field(None, alias="_id")
    modified_timestamp: Optional[datetime] = None
    created_timestamp: Optional[datetime] = None

    class Config:
        populate_by_name = True


class TodayResponse(BaseModel):
    value: Optional[DailySelfReportStorage] = None
    error: Optional[str] = None


TODAY_MISSING_RESPONSE = TodayResponse(error="Report not found")
