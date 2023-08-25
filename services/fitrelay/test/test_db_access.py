from models import Token
from db import insert_token_to_db, get_token_from_db, create_db_if_needed


def main():
    create_db_if_needed()
    fake_token = Token(
        access_token="fake_access_token",
        refresh_token="fake_refresh_token",
        user_id="fake_user_id",
        user_profile={"fake": "user_profile"},
    )

    insert_token_to_db(fake_token)
    token = get_token_from_db(1)

    print(token)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
