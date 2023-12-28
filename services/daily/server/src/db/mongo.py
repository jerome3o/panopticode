from typing import List, Optional
from datetime import datetime, timedelta, time
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from constants import MONGODB_COLLECTION_NAME
from models import (
    DailySelfReportStorage,
    DailySelfReportTransfer,
    TodayResponse,
    TODAY_MISSING_RESPONSE,
)
from db.model import DailySelfReportDB


class DailySelfReportMongoDB(DailySelfReportDB):
    def __init__(self, conn_str, db_name):
        self.client = AsyncIOMotorClient(conn_str)
        self.collection = self.client[db_name][MONGODB_COLLECTION_NAME]

    async def initialise(self):
        pass

    async def create_report(self, record: DailySelfReportTransfer) -> str:
        storage_record = DailySelfReportStorage.model_validate(
            record.model_dump(),
        )
        storage_record.modified_timestamp = datetime.now()
        storage_record.created_timestamp = datetime.now()
        result = await self.collection.insert_one(storage_record.model_dump())
        storage_record.id = str(result.inserted_id)
        return storage_record

    async def get_reports(self) -> List[DailySelfReportStorage]:
        cursor = self.collection.find()
        return [
            DailySelfReportStorage.model_validate(record) async for record in cursor
        ]

    async def update_report(
        self, id: str, record: DailySelfReportTransfer
    ) -> Optional[DailySelfReportStorage]:
        storage_record = DailySelfReportStorage.model_validate(record.model_dump())
        storage_record.modified_timestamp = datetime.now()

        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": storage_record.model_dump(
                    exclude_none=True,
                    exclude_unset=True,
                )
            },
        )

        if result.modified_count:
            storage_record.id = id
            return storage_record
        return None

    async def get_todays_report(self) -> TodayResponse:
        today = datetime.combine(datetime.now().date(), time())
        result = await self.collection.find_one(
            {
                "created_timestamp": {
                    "$gte": today,
                    "$lt": today + timedelta(days=1),
                },
            },
        )
        if result:
            return TodayResponse(value=result)
        return TODAY_MISSING_RESPONSE

    async def close(self):
        self.client.close()
