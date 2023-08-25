"""
Handles all the database related queries and setup.
"""
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    JSON,
    inspect,
)

from models import Token

engine = create_engine("sqlite:///users.db", echo=True)
meta = MetaData()

tokens = Table(
    "Tokens",
    meta,
    Column("id", Integer, primary_key=True),
    Column("access_token", String),
    Column("refresh_token", String),
    # user_id
    Column("user_id", String),
    # user profile data
    Column("user_profile", JSON),
)


def create_db():
    meta.create_all(engine)


def create_db_if_needed():
    if not inspect(engine).has_table(engine, "Tokens"):
        create_db()


def insert_token_to_db(token: Token):
    conn = engine.connect()
    insert_op = tokens.insert().values(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        user_id=token.user_id,
        user_profile=token.user_profile,
    )
    conn.execute(insert_op)
    conn.commit()
    conn.close()


def get_token_from_db(token_id: int) -> Token:
    conn = engine.connect()
    select_query = tokens.select().where(tokens.c.id == token_id)
    values = conn.execute(select_query).fetchone()
    conn.close()
    return Token(
        access_token=values[1],
        refresh_token=values[2],
        user_id=values[3],
        user_profile=values[4],
    )
