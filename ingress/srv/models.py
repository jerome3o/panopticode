from pydantic import BaseModel


class Transaction(BaseModel):
    account: str
    date: str
    transaction_id: int
    transaction_type: str
    payee: str
    memo: str
    amount: float
