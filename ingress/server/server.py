from pydantic import BaseModel
from fastapi import FastAPI, Body


app = FastAPI()


class Statement(BaseModel):
    text: str


@app.post('/bank-statement')
def bank_statement_ingress(statement: Statement):
    print(statement.text)
    return "ok"