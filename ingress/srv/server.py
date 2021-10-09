from pydantic import BaseModel
from fastapi import FastAPI

from srv.parser import parse_statement
from srv.models import Transaction

from apitools.service import configure_api
from apitools.mongodb import MongoCrud, get_client


app = FastAPI()


class Statement(BaseModel):
    text: str


client = get_client()
crud = MongoCrud(
    model=Transaction,
    collection=client["panopticon"]["bank"],
)
configure_api(app, crud, Transaction, "/transactions")


@app.post('/bank-statement')
def bank_statement_ingress(statement: Statement):
    transactions = parse_statement(statement.text)
    for transaction in transactions:
        crud.idempotent_create(transaction)
    return {"result": "success"}