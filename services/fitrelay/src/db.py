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
    # Column("user_id", String),
    # user_id should be the primary key
    Column("user_id", String, primary_key=True),
    Column("access_token", String),
    Column("refresh_token", String),
    # user profile data
    Column("user_profile", JSON),
)


def create_db():
    meta.create_all(engine)


def create_db_if_needed():
    if not inspect(engine).has_table("Tokens"):
        print("creating db")
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
        access_token=values["access_token"],
        refresh_token=values["refresh_token"],
        user_id=values["user_id"],
        user_profile=values["user_profile"],
    )
