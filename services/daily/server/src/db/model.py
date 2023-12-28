from abc import ABC, abstractmethod
from typing import List, Optional

from models import (
    DailySelfReportStorage,
    DailySelfReportTransfer,
    TodayResponse,
)


class DailySelfReportDB(ABC):
    @abstractmethod
    async def initialise():
        pass

    @abstractmethod
    async def create_report(self, record: DailySelfReportTransfer) -> str:
        pass

    @abstractmethod
    async def get_reports(self) -> List[DailySelfReportStorage]:
        pass

    @abstractmethod
    async def update_report(
        self, id: str, record: DailySelfReportTransfer
    ) -> Optional[DailySelfReportStorage]:
        pass

    @abstractmethod
    async def get_todays_report(self) -> TodayResponse:
        pass

    @abstractmethod
    async def close(self):
        self.client.close()
