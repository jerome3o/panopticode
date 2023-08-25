"""
Handles all the database related queries and setup.
"""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine("sqlite:///users.db", echo=True)
meta = MetaData()

tokens = Table(
    "Tokens",
    meta,
    Column("id", Integer, primary_key=True),
    Column("access_token", String),
    Column("refresh_token", String),
)


def insert_token(access_token: str, refresh_token: str):
    conn = engine.connect()
    insert_op = tokens.insert().values(
        access_token=access_token, refresh_token=refresh_token
    )
    conn.execute(insert_op)


def get_token(token_id: int):
    conn = engine.connect()
    select_query = tokens.select().where(tokens.c.id == token_id)
    return conn.execute(select_query).fetchone()
