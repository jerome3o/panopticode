from typing import List
from models import Transaction
import pandas as pd
from io import StringIO

BANK_LINE = 1
FIRST_TRANSACTION_LINE = 8


def parse_statement(statement: str) -> List[Transaction]:
    transactions: List[Transaction] = []
    account = _get_bank_account_string_from_line(statement.split("\n")[BANK_LINE])
    df = pd.read_csv(StringIO(statement), skiprows=FIRST_TRANSACTION_LINE-1)
    df.columns = [
        "date",
        "transaction_id",
        "transaction_type",
        "cheque_number",
        "payee",
        "memo",
        "amount",
    ]
    transactions = [
        Transaction(
            account=account,
            **dict(row)
        )
        for _, row in df.iterrows()
    ]
    return transactions



def _get_bank_account_string_from_line(line: str) -> str:
    bank_id, branch_id, account_id, *_ = line.split(";")
    bank_id = bank_id.strip().split(" ")[1]
    branch_id = branch_id.strip().split(" ")[1]
    account_id = account_id.strip().split(" ")[1]
    return "-".join([bank_id, branch_id, account_id])

