from db import get_all_tokens_from_db
from auth import refresh_token


def main():
    tokens = get_all_tokens_from_db()
    for token in tokens:
        refresh_token(token)
        break


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
