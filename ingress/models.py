from pydantic import BaseModel, Field


class Transaction(BaseModel):
    account: str
    date: str
    transaction_id: int
    transaction_type: str
    payee: str
    memo: str
    amount: float


class ChromeHistoryItem(BaseModel):
    chrome_id: str = Field(alias="id")
    last_visit_time: float = Field(alias="lastVisitTime")
    title: str = Field(alias="title")
    url: str = Field(alias="url")
    typed_count: int = Field(alias="typedCount")
    visit_count: int = Field(alias="visitCount")

    class Config:
        allow_population_by_field_name = True
