from typing import List, Optional
from datetime import datetime, timedelta
import sqlite3

from models import (
    DailySelfReportStorage,
    DailySelfReportTransfer,
    TodayResponse,
    TODAY_MISSING_RESPONSE,
)
from db.model import DailySelfReportDB


def get_report_storage(row):
    value = DailySelfReportStorage.model_validate_json(row[1])
    value.id = str(row[0])
    return value


class DailySelfReportSQLite(DailySelfReportDB):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    async def initialise(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL
            )
        """
        )
        self.conn.commit()

    async def create_report(
        self, record: DailySelfReportTransfer
    ) -> DailySelfReportStorage:
        storage_record = DailySelfReportStorage.model_validate(
            record.model_dump(),
        )
        storage_record.modified_timestamp = datetime.now()
        storage_record.created_timestamp = datetime.now()

        data = storage_record.model_dump_json()

        cursor = self.conn.execute("INSERT INTO reports (data) VALUES (?)", (data,))
        self.conn.commit()

        storage_record.id = str(cursor.lastrowid)
        return storage_record

    async def get_reports(self) -> List[DailySelfReportStorage]:
        cursor = self.conn.execute("SELECT id, data FROM reports")

        return [get_report_storage(row) for row in cursor]

    async def update_report(
        self, id: str, record: DailySelfReportTransfer
    ) -> Optional[DailySelfReportStorage]:
        new_report_content = DailySelfReportTransfer.model_validate(
            record.model_dump(),
        )

        cursor = self.conn.execute("SELECT id, data FROM reports WHERE id=?", (id,))
        row = cursor.fetchone()

        if row is None:
            # todo: raise exception?
            return None

        existing_report = get_report_storage(row)
        existing_report.report = new_report_content.report

        data = existing_report.model_dump_json()

        cursor = self.conn.execute("UPDATE reports SET data=? WHERE id=?", (data, id))
        self.conn.commit()
        if cursor.rowcount > 0:
            value = DailySelfReportStorage.model_validate_json(data)
            value.id = id
            return value
        else:
            return None

    async def get_todays_report(self) -> TodayResponse:
        today = datetime.now().date()
        cursor = self.conn.execute(
            "SELECT id, data FROM reports WHERE "
            + "datetime(json_extract(data, '$.created_timestamp')) >= ? AND "
            + "datetime(json_extract(data, '$.created_timestamp')) < ?",
            (today.isoformat(), (today + timedelta(days=1)).isoformat()),
        )
        row = cursor.fetchone()
        if row is None:
            return TODAY_MISSING_RESPONSE
        else:
            value = DailySelfReportStorage.model_validate_json(row[1])
            value.id = str(row[0])
            return TodayResponse(value=value)

    async def close(self):
        self.conn.close()
