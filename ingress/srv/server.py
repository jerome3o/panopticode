from pydantic import BaseModel
from fastapi import FastAPI

from srv.parser import parse_statement
from models import ChromeHistoryItem, Transaction

from apitools.service import configure_api
from apitools.mongodb import MongoCrud, get_client


app = FastAPI()


class Statement(BaseModel):
    text: str


client = get_client()
transaction_crud = MongoCrud(
    model=Transaction,
    collection=client["panopticon"]["bank"],
)
browsing_history_crud = MongoCrud(
    model=ChromeHistoryItem,
    collection=client["panopticon"]["chrome"],
)

configure_api(app, transaction_crud, Transaction, "/transactions")
configure_api(app, browsing_history_crud, ChromeHistoryItem, "/browsing_history")


@app.post("/bank-statement")
def bank_statement_ingress(statement: Statement):
    transactions = parse_statement(statement.text)
    for transaction in transactions:
        transaction_crud.idempotent_create(transaction)
    return {"result": "success"}
