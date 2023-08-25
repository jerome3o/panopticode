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

from models import TokenInfo

engine = create_engine("sqlite:///users.db", echo=True)
meta = MetaData()

tokens = Table(
    "Tokens",
    meta,
    # Column("user_id", String),
    # user_id should be the primary key
    Column("user_id", String, primary_key=True),
    # user profile data
    Column("user_profile", JSON),
    Column("token_response", JSON),
    # created unix timestamp
    Column("created", Integer),
)


def create_db():
    meta.create_all(engine)


def create_db_if_needed():
    if not inspect(engine).has_table("Tokens"):
        create_db()


def insert_token_to_db(token: TokenInfo):
    conn = engine.connect()

    # TODO(j.swannack): needs revisiting - update if exists, insert if not
    # delete all rows with the user_id
    conn.execute(tokens.delete().where(tokens.c.user_id == token.user_id))

    insert_op = tokens.insert().values(
        user_id=token.user_id,
        user_profile=token.user_profile,
        token_response=token.token_response.model_dump(),
        created=token.created,
    )
    conn.execute(insert_op)
    conn.commit()
    conn.close()


def get_token_from_db(token_id: int) -> TokenInfo:
    conn = engine.connect()
    select_query = tokens.select().where(tokens.c.id == token_id)
    values = conn.execute(select_query).fetchone()
    conn.close()
    return TokenInfo(
        user_id=values["user_id"],
        user_profile=values["user_profile"],
        token_response=values["token_response"],
        created=values["created"],
    )
